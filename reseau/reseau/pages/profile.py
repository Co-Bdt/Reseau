from typing import Dict
import boto3
from pathlib import Path
from random import shuffle
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..components.profile_text import profile_text
from ..components.interest_badges import interest_badges
from ..models import (
    Interest,
    Preference,
    UserAccount,
    UserInterest,
    UserPreference,
)
from ..reseau import PROFILE_ROUTE
from rxconfig import S3_BUCKET_NAME


class ProfileState(BaseState):
    profile_text: str = ''  # the user's profile text
    profile_pic: str = ''  # the user's profile image name
    interests_names: list[str] = []  # all interests names
    # the user's selected interests names
    selected_interests_names: list[str] = []
    user_pref: Dict[str, bool] = {  # the user's enabled preferences
        "post_notif_enabled": False,
        "pm_notif_enabled": False,
    }

    def set_user_pref(self, key: str, value: bool):
        self.user_pref[key] = value

    def init(self):
        self.profile_text = self.authenticated_user.profile_text
        yield

        if self.authenticated_user.profile_picture:
            self.profile_pic = self.authenticated_user.profile_picture
        else:
            self.profile_pic = "blank_profile_picture"
        yield

        # Load interests from database
        with rx.session() as session:
            interests = session.exec(
                Interest.select().order_by(Interest.name)
            ).all()
        self.interests_names = [interest.name for interest in interests]
        shuffle(self.interests_names)

        # Load the user's interests
        with rx.session() as session:
            user_interests = session.exec(
                UserInterest.select()
                .options(
                    sa.orm.selectinload(UserInterest.interest)
                )
                .where(
                    UserInterest.useraccount_id == self.authenticated_user.id
                )
            ).all()
            self.selected_interests_names = [
                interest.interest.name for interest in user_interests
            ]

        # Load the user's preferences
        with rx.session() as session:
            user = session.exec(
                UserAccount.select()
                .options(
                    sa.orm.selectinload(UserAccount.preference_list)
                    .selectinload(UserPreference.preference)
                )
                .where(
                    UserAccount.id == self.authenticated_user.id
                )
            ).first()

        for pref in user.preference_list:
            self.user_pref[pref.preference.name] = True

    async def handle_upload(self, files: list[rx.UploadFile]):
        '''Handle the upload of file(s).

        Args:
            files: The uploaded file(s).
        '''

        for file in files:
            upload_data = await file.read()
            outfile = (
                rx.get_upload_dir() /
                f"{self.authenticated_user.id}" /
                file.filename
            )

            # Create the user's directory if it doesn't exist
            Path(
                rx.get_upload_dir() /
                f"{self.authenticated_user.id}"
            ).mkdir(parents=True, exist_ok=True)

            # Save the file.
            with outfile.open('wb') as file_object:
                file_object.write(upload_data)

            # Update the profile_img var.
            self.profile_pic = (
                f"{self.authenticated_user.id}/" +
                f"{file.filename}"
            )

    def add_selected(self, item: str):
        # limit selected items to 4
        if len(self.selected_interests_names) < 4:
            self.selected_interests_names.append(item)
        else:
            return rx.toast.warning("Tu ne peux sélectionner que 4 intérêts.")

    def remove_selected(self, item: str):
        if len(self.selected_interests_names) > 2:
            self.selected_interests_names.remove(item)
        else:
            return rx.toast.warning(
                "Tu dois sélectionner au moins 2 intérêts."
            )

    def update_profile_picture(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)

        try:
            # Upload the profile picture to S3
            bucket.upload_file(
                f"{rx.get_upload_dir()}/{self.profile_pic}",
                self.profile_pic,
            )
        except Exception:
            pass

        # Remove the old profile picture starting with the user's id
        # from the file system (old system of storing profile pictures)
        import fnmatch
        import os
        filepath = rx.get_upload_dir()
        try:
            for file in os.listdir(filepath):
                if fnmatch.fnmatch(file, f"{self.authenticated_user.id}_*"):
                    os.remove(filepath / file)
        except Exception:
            pass

        try:
            bucket.download_file(
                self.profile_pic,
                rx.get_upload_dir() / f"{self.profile_pic}",
            )
            self.profile_pic = (
                f"{self.profile_pic}"
            )
        except Exception:
            self.profile_pic = "blank_profile_picture"

    def update_interests(self):
        # Get the corresponding interest objects from the database
        # and store their ids in a list
        selected_interests: list[Interest] = []
        with rx.session() as session:
            selected_interests = session.exec(
                Interest.select()
                .where(Interest.name.in_(self.selected_interests_names))
            ).all()
        selected_interests_ids = [
            str(interest.id) for interest in selected_interests
        ]

        # Update the authenticated user's interests in the joint table
        with rx.session() as session:
            user_interests = session.exec(
                UserInterest.select().where(
                    UserInterest.useraccount_id == self.authenticated_user.id
                )
            ).all()
            for user_interest in user_interests:
                session.delete(user_interest)

            for interest_id in selected_interests_ids:
                user_interest = UserInterest(
                    useraccount_id=self.authenticated_user.id,
                    interest_id=interest_id
                )
                session.add(user_interest)
            session.commit()

    def update_preferences(self):
        # Retrieve all preferences
        with rx.session() as session:
            preferences = session.exec(
                Preference.select()
            ).all()

        # If the pref is enabled, add a UserPreference record
        # else try to remove
        with rx.session() as session:
            for pref in preferences:
                if self.user_pref[pref.name]:
                    user_pref = UserPreference(
                        useraccount_id=self.authenticated_user.id,
                        preference_id=pref.id
                    )
                    session.add(user_pref)
                else:
                    user_pref = session.exec(
                        UserPreference.select()
                        .where(
                            (UserPreference.useraccount_id ==
                                self.authenticated_user.id) &
                            (UserPreference.preference_id == pref.id)
                        )
                    ).first()
                    if user_pref:
                        session.delete(user_pref)
            session.commit()

    def save_profile(self) -> rx.event.EventSpec:
        # Update the profile picture
        self.update_profile_picture()

        profile_text_cleaned = self.authenticated_user.clean_profile_text(
            self.profile_text
        )
        # Retrieve the authenticated user with its id and update it
        with rx.session() as session:
            user: UserAccount = session.exec(
                UserAccount.select().where(
                    UserAccount.id == self.authenticated_user.id
                )
            ).first()
            user.profile_text = profile_text_cleaned
            user.profile_picture = self.profile_pic

            session.add(user)
            session.commit()
        # Update the user's profile text visually
        self.set_profile_text(profile_text_cleaned)

        # Update the user's interests
        self.update_interests()

        # Update the user's preferences
        self.update_preferences()

        return rx.toast.success("Profil mis à jour.")


@rx.page(title="Profil", route=PROFILE_ROUTE, on_load=ProfileState.init)
@template
def profile_page() -> rx.Component:
    '''
    Render the user's profile page.

    Returns:
        A reflex component.
    '''
    return rx.cond(
        ProfileState.is_hydrated,
        rx.vstack(
            rx.tablet_and_desktop(
                rx.hstack(
                    rx.upload(
                        rx.image(
                            src=rx.get_upload_url(
                                ProfileState.profile_pic
                            ),
                            width=['7.75em'],
                            height=['7.75em'],
                            border_radius='50%',
                            object_fit="cover",
                        ),
                        id='profile_img',
                        multiple=False,
                        accept={
                            'image/png': ['.png'],
                            'image/jpeg': ['.jpg', '.jpeg'],
                        },
                        on_drop=ProfileState.handle_upload(
                            rx.upload_files(upload_id='profile_img')
                        ),
                        padding='0',
                        width=['9em'],
                        height=['7.75em'],
                        border='none',
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text(
                                ProfileState.authenticated_user.first_name,
                                style=rx.Style(
                                    font_weight='600',
                                    font_size='1.2em',
                                ),
                            ),
                            rx.text(
                                ProfileState.authenticated_user.last_name,
                                style=rx.Style(
                                    font_weight='600',
                                    font_size='1.2em',
                                ),
                            ),
                            spacing='1',
                        ),
                        profile_text(
                            ProfileState.profile_text,
                            ProfileState.set_profile_text
                        ),
                        width='100%',
                    ),
                    width='100%',
                    align='start',
                ),
                width='100%',
                margin_bottom='1em',
            ),
            rx.mobile_only(
                rx.vstack(
                    rx.hstack(
                        rx.upload(
                            rx.image(
                                src=rx.get_upload_url(
                                    ProfileState.profile_pic
                                ),
                                width=['4em'],
                                height=['4em'],
                                border_radius='50%',
                                object_fit="cover",
                            ),
                            id='profile_img',
                            multiple=False,
                            accept={
                                'image/png': ['.png'],
                                'image/jpeg': ['.jpg', '.jpeg'],
                            },
                            on_drop=ProfileState.handle_upload(
                                rx.upload_files(upload_id='profile_img')
                            ),
                            margin_right='0.5em',
                            padding='0',
                            height=['4em'],
                            border='none',
                        ),
                        rx.text(
                            ProfileState.authenticated_user.first_name,
                            style=rx.Style(
                                font_weight='600',
                                font_size='1.1em',
                            ),
                        ),
                        rx.text(
                            ProfileState.authenticated_user.last_name,
                            style=rx.Style(
                                font_weight='600',
                                font_size='1.1em',
                            ),
                        ),
                        spacing='1',
                    ),
                    profile_text(
                        ProfileState.profile_text,
                        ProfileState.set_profile_text
                    ),
                ),
                width='100%',
                margin_bottom='1em',
            ),

            rx.heading(
                "Intérêts",
                margin='0 0 0.5em 0',
            ),
            rx.desktop_only(
                interest_badges(
                    interests_names=ProfileState.interests_names,
                    selected_interests_names=ProfileState.selected_interests_names,  # noqa: E501
                    add_selected=ProfileState.add_selected,
                    remove_selected=ProfileState.remove_selected,
                    badge_size='3',
                ),
            ),
            rx.mobile_and_tablet(
                interest_badges(
                    interests_names=ProfileState.interests_names,
                    selected_interests_names=ProfileState.selected_interests_names,  # noqa: E501
                    add_selected=ProfileState.add_selected,
                    remove_selected=ProfileState.remove_selected,
                    badge_size='2',
                ),
            ),

            rx.vstack(
                # rx.flex(
                #     rx.switch(
                #         default_checked=False,
                #         checked=ProfileState.notif_checked,
                #         on_change=ProfileState.set_notif_checked
                #     ),
                rx.text("Notifications par mail"),
                #     spacing='2',
                # ),
                rx.vstack(
                    rx.flex(
                        rx.switch(
                            checked=ProfileState.user_pref[
                                'post_notif_enabled'
                            ],
                            on_change=lambda v: ProfileState.set_user_pref(
                                'post_notif_enabled', v
                            )
                        ),
                        rx.text("Posts"),
                        spacing='2',
                    ),
                    rx.flex(
                        rx.switch(
                            checked=ProfileState.user_pref['pm_notif_enabled'],
                            on_change=lambda v: ProfileState.set_user_pref(
                                'pm_notif_enabled', v
                            )
                        ),
                        rx.text("Messages privés"),
                        spacing='2',
                    ),
                    # margin_left='2em'
                ),
            ),

            rx.hstack(
                rx.button(
                    "Valider",
                    size='3',
                    on_click=ProfileState.save_profile
                ),
                rx.link(
                    "Se déconnecter",
                    underline='none',
                    href='/',
                    on_click=BaseState.do_logout,
                ),
                width='100%',
                justify='between',
                align='center',
                margin_top='1em',
            ),
        ),
    ),
