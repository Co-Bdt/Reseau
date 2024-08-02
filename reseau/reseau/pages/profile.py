import boto3
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..components.profile_text import profile_text
from ..components.profile_chips import profile_chips
from ..models import Interest, UserAccount, UserInterest
from ..reseau import PROFILE_ROUTE, S3_BUCKET_NAME


class ProfileState(BaseState):
    profile_text: str = ""  # the user's profile text
    profile_img: str = ""  # the user's profile image name
    # the user's selected interests names
    selected_interests_names: list[str] = []

    def init(self):
        self.profile_text = self.authenticated_user.profile_text

        # Load the user's profile picture from S3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)
        try:
            bucket.download_file(
                f"{self.authenticated_user.id}/profile_picture",
                rx.get_upload_dir() /
                f"{self.authenticated_user.id}_profile_picture.png",
            )
            self.profile_img = (
                f"{self.authenticated_user.id}_"
                "profile_picture.png"
            )
        except Exception:
            self.profile_img = "blank_profile_picture.png"

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

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded file(s).
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the profile_img var.
            self.profile_img = file.filename

    def add_selected(self, item: str):
        # limit selected items to 2
        if len(self.selected_interests_names) < 2:
            self.selected_interests_names.append(item)
        else:
            return rx.toast.warning("Tu ne peux sélectionner que 2 intérêts.")

    def remove_selected(self, item: str):
        self.selected_interests_names.remove(item)

    def update_profile_picture(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)

        # Upload the profile picture to S3
        bucket.upload_file(
            f"{rx.get_upload_dir()}/{self.profile_img}",
            f"{self.authenticated_user.id}/profile_picture"
        )

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
            # session.commit()

            for interest_id in selected_interests_ids:
                user_interest = UserInterest(
                    useraccount_id=self.authenticated_user.id,
                    interest_id=interest_id
                )
                session.add(user_interest)
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
            session.add(user)
            session.commit()
        # Update the user's profile text visually
        self.set_profile_text(profile_text_cleaned)

        # Update the user's interests
        self.update_interests()

        return rx.toast.success("Profil mis à jour.")


@rx.page(title="Profil", route=PROFILE_ROUTE, on_load=ProfileState.init)
@template
def profile_page() -> rx.Component:
    return rx.cond(
        ProfileState.is_hydrated,
        rx.vstack(
            rx.hstack(
                rx.heading(
                    "Ton profil",
                    size="5",
                    style=rx.Style(
                        margin_bottom="1em"
                    ),
                ),
                rx.color_mode.button(),
                width="100%",
                justify="between",
            ),
            rx.hstack(
                rx.upload(
                    rx.image(
                        src=rx.get_upload_url(ProfileState.profile_img),
                        width="9vh",
                        height="9vh",
                        border="1px solid #ccc",
                        border_radius="50%",
                    ),
                    id="profile_img",
                    padding="0px",
                    width="10vh",
                    height="10vh",
                    border="none",
                    multiple=False,
                    accept={
                        "image/png": [".png"],
                        "image/jpeg": [".jpg", ".jpeg"],
                    },
                    on_drop=ProfileState.handle_upload(
                        rx.upload_files(upload_id="profile_img")
                    ),
                ),
                profile_text(
                    ProfileState.profile_text,
                    ProfileState.set_profile_text
                ),
                width="100%",
                margin_bottom="1em",
            ),
            profile_chips(
                selected_interests=ProfileState.selected_interests_names,
                add_selected=ProfileState.add_selected,
                remove_selected=ProfileState.remove_selected,
            ),
            rx.hstack(
                rx.button(
                    "Valider",
                    size="3",
                    on_click=ProfileState.save_profile
                ),
                rx.link(
                    "Se déconnecter",
                    underline="none",
                    href="/",
                    on_click=BaseState.do_logout,
                ),
                width="100%",
                justify="between",
                align="center",
                margin_top="1em",
            ),
            width="100%",
        ),
    ),
