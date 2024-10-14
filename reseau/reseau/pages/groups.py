from pathlib import Path
from random import shuffle
import re
import boto3
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..components.interest_badges import interest_badges
from ..models import Group, Interest, UserGroup
from ..reseau import GROUPS_ROUTE
from rxconfig import S3_BUCKET_NAME


class GroupsState(rx.State):
    # Var containing a list of public groups and their group name, number of members, is user in group  # noqa: E501
    public_groups_displayed: list[tuple[Group, str, int, bool]] = []
    # Var containing a list of user's group and their group, group name, number of members  # noqa: E501
    user_groups_displayed: list[tuple[Group, str, int]] = []
    interests_names: list[str] = []

    new_group_image: str = ""
    new_group_name: str = ""
    new_group_interest_name: list[str] = []

    async def init(self):
        await self.load_groups()
        self.new_group_image: str = "blank_group_image"
        self.new_group_name: str = ""
        self.new_group_interest_name: list[str] = []

    async def load_groups(self):
        # Groups the user is part of
        self.user_groups_displayed = []
        base_state = await self.get_state(BaseState)
        with rx.session() as session:
            user_groups = session.exec(
                Group.select()
                .join(UserGroup)
                .options(
                    sa.orm.selectinload(Group.interest),
                    sa.orm.selectinload(Group.user_group_list)
                    .selectinload(UserGroup.useraccount)
                )
                .where(
                    UserGroup.useraccount_id ==
                    base_state.authenticated_user.id
                )
            ).all()

        for group in user_groups:
            self.user_groups_displayed.append(
                (group,
                 Group.from_url_name(group.name),
                 len(group.user_group_list))
            )

        # Public groups
        self.public_groups_displayed = []
        with rx.session() as session:
            public_groups = session.exec(
                Group.select()
                .options(
                    sa.orm.selectinload(Group.interest),
                    sa.orm.selectinload(Group.user_group_list)
                    .selectinload(UserGroup.useraccount)
                )
            ).all()
        for group in public_groups:
            self.public_groups_displayed.append(
                (group,
                 Group.from_url_name(group.name),
                 len(group.user_group_list),
                 (group.id in [group.id for group in user_groups]))  # Check if the current group is in the user's groups  # noqa: E501
            )
        # Display public groups in random order.
        shuffle(self.public_groups_displayed)

    async def join_group(self, group: Group):
        base_state = await self.get_state(BaseState)

        with rx.session() as session:
            usergroup = session.exec(
                UserGroup.select()
                .where(
                    UserGroup.useraccount_id ==
                    base_state.authenticated_user.id
                )
                .where(UserGroup.group_id == group['id'])
            ).first()
            if usergroup:
                return rx.toast.warning("Tu es déjà membre de cette Fratrie.")
            if len(group['user_group_list']) >= group['max_members']:
                return rx.toast.warning(
                    "Désolé, cette Fratrie est au complet."
                )

        usergroup = UserGroup(
            useraccount_id=base_state.authenticated_user.id,
            group_id=group['id']
        )
        with rx.session() as session:
            session.add(usergroup)
            session.commit()
        return rx.redirect(f"{GROUPS_ROUTE}/{group['name']}")

    def handle_dialog_open(self):
        # Load interests from database for group creation
        with rx.session() as session:
            interests = session.exec(
                Interest.select().order_by(Interest.name)
            ).all()
        self.interests_names = [interest.name for interest in interests]
        shuffle(self.interests_names)

    def add_selected(self, item: str):
        # limit selected items to 1
        if len(self.new_group_interest_name) < 1:
            self.new_group_interest_name.append(item)
        else:
            return rx.toast.warning("Tu ne peux sélectionner qu'un intérêt.")

    def remove_selected(self, item: str):
        if len(self.new_group_interest_name) > 0:
            self.new_group_interest_name.remove(item)
        else:
            return rx.toast.warning(
                "Tu dois sélectionner au moins 1 intérêt."
            )

    async def handle_upload(self, files: list[rx.UploadFile]):
        '''Handle the upload of file(s).

        Args:
            files: The uploaded file(s).
        '''
        file = files[0]

        # Read uploaded file and prepare to save it
        upload_data = await file.read()
        outfile = (
            rx.get_upload_dir() / file.filename
        )

        # Save the file
        with outfile.open('wb') as file_object:
            file_object.write(upload_data)

        # Update the group_image var
        self.new_group_image = file.filename

    async def create_group(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)
        base_state = await self.get_state(BaseState)

        # Regex to check if the group name is composed of at least 3 letters
        regex = re.compile(r'^[a-zA-Z ]{3,20}$')
        if not regex.match(self.new_group_name):
            return rx.toast.warning(
                "Le nom de ta Fratrie doit contenir entre 3 et 20 lettres."
            )
        if not self.new_group_interest_name:
            return rx.toast.warning(
                "Ta Fratrie doit être autour d'un intérêt."
            )
        if self.new_group_image == "blank_group_image":
            return rx.toast.warning(
                "Ta Fratrie doit avoir une image."
            )

        with rx.session() as session:
            interest = session.exec(
                Interest.select()
                .where(Interest.name == self.new_group_interest_name[0])
            ).first()
        new_group = Group(
            name=Group.to_url_name(self.new_group_name),
            interest_id=interest.id,
        )

        # Create the group and add the current user as owner
        try:
            with rx.session() as session:
                session.add(new_group)
                session.commit()
                session.refresh(new_group)

                # Set the group image with its id as prefix.
                new_group.image = (
                    f'group_{new_group.id}/' +
                    f'{self.new_group_image}'
                )
                session.commit()
                session.refresh(new_group)

                # Upload the image to S3
                bucket.upload_file(
                    rx.get_upload_dir() / self.new_group_image,
                    f'group_{new_group.id}/' +
                    f'{self.new_group_image}'
                )

                # Create the group's directory if it doesn't exist
                Path(
                    rx.get_upload_dir() /
                    f"group_{new_group.id}"
                ).mkdir(parents=True, exist_ok=True)

                # Download the image to make it available for the app
                bucket.download_file(
                    f'group_{new_group.id}/' +
                    f'{self.new_group_image}',
                    rx.get_upload_dir() / new_group.image
                )

                # Add the user as owner of the group
                user_group = UserGroup(
                    useraccount_id=base_state.authenticated_user.id,
                    group_id=new_group.id,
                    is_owner=True,
                )
                session.add(user_group)
                session.commit()
                return rx.redirect(f'{GROUPS_ROUTE}/{new_group.name}')
        except Exception:
            return rx.toast.warning(
                "Une erreur s'est produite lors de la création de ta Fratrie."
            )


@rx.page(title="Fratries", route=GROUPS_ROUTE, on_load=GroupsState.init)
@template
def groups_page() -> rx.Component:
    """
    Render the groups page which allow users to \
        - search for groups by interest
        - join a group

    Returns:
        A reflex component.
    """
    return rx.cond(
        GroupsState.is_hydrated,
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.text("Fratries", width='100%'),
                    rx.dialog.root(
                        rx.dialog.trigger(
                            rx.button(
                                "Créer",
                                width='100px',
                                on_click=GroupsState.handle_dialog_open,
                            )
                        ),
                        rx.dialog.content(
                            rx.dialog.title("Nouvelle Fratrie"),
                            rx.hstack(
                                rx.upload(
                                    rx.image(
                                        src=rx.get_upload_url(
                                            GroupsState.new_group_image
                                        ),
                                        width=['5em'],
                                        height=['5em'],
                                        border_radius='50%',
                                        object_fit="cover",
                                    ),
                                    id='profile_img',
                                    multiple=False,
                                    accept={
                                        'image/png': ['.png'],
                                        'image/jpeg': ['.jpg', '.jpeg'],
                                    },
                                    on_drop=GroupsState.handle_upload(
                                        rx.upload_files(upload_id='group_img')
                                    ),
                                    padding='0',
                                    width='6em',
                                    height='5em',
                                    border='none',
                                ),
                                rx.input(
                                    placeholder="Nom de la Fratrie",
                                    value=GroupsState.new_group_name,
                                    on_change=GroupsState.set_new_group_name,
                                ),
                            ),
                            interest_badges(
                                interests_names=GroupsState.interests_names,
                                selected_interests_names=GroupsState.new_group_interest_name,  # noqa: E501
                                add_selected=GroupsState.add_selected,
                                remove_selected=GroupsState.remove_selected,
                                badge_size='2',
                            ),
                            rx.flex(
                                rx.dialog.close(
                                    rx.button(
                                        "Annuler",
                                        color_scheme="gray",
                                        variant="soft",
                                    ),
                                ),
                                rx.button(
                                    "Créer",
                                    on_click=GroupsState.create_group,
                                ),
                                justify="end",
                                spacing="3",
                                margin_top="16px",
                            ),
                        ),
                    ),
                ),
                rx.desktop_only(
                    rx.grid(
                        rx.foreach(
                            GroupsState.public_groups_displayed,
                            lambda group: rx.card(
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.image(
                                                src=rx.get_upload_url(
                                                    group[0].image
                                                ),
                                                width=['5em'],
                                                height=['5em'],
                                                border_radius='50%',
                                                object_fit="cover",
                                            ),
                                            rx.vstack(
                                                rx.text(group[1]),
                                                rx.hstack(
                                                    rx.text(
                                                        f"{group[2]}/{group[0].max_members} membres"
                                                    ),
                                                    rx.text(group[0].interest.name),
                                                ),
                                            ),
                                        ),
                                        rx.cond(
                                            ~group[3],
                                            rx.button(
                                                "Rejoindre",
                                                on_click=GroupsState.join_group(
                                                    group[0]
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        columns='3',
                    )
                ),
                # rx.tablet_only(
                # ),
                # rx.mobile_only(
                # ),
                width='85%',
            ),
            rx.vstack(
                rx.text("Mes Fratries"),
                rx.grid(
                    rx.foreach(
                        GroupsState.user_groups_displayed,
                        lambda group: rx.card(
                            rx.box(
                                rx.text(group[1]),
                                rx.hstack(
                                    rx.text(
                                        f"{group[2]}/{group[0].max_members} membres"
                                    ),
                                    rx.text(group[0].interest.name),
                                ),
                            ),
                            cursor='pointer',
                            on_click=rx.redirect(
                                f"{GROUPS_ROUTE}/{group[0].name}"
                            ),
                        ),
                    ),
                    columns='1',
                ),
                justify='start',
                width='15%',
            )
        )
    )
