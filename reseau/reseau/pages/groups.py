from pathlib import Path
from random import shuffle
import re
import boto3
import reflex as rx
import sqlalchemy as sa


from ..common.base_state import BaseState
from ..common.template import template
from ..components.common.interest_chip import interest_chip
from ..components.groups.group_interest_filter import group_interest_filter
from ..components.groups.new_group_dialog import new_group_dialog
from ..components.groups.public_groups_grid import public_groups_grid
from ..models import Group, Interest, UserGroup
from ..reseau import GROUPS_ROUTE
from rxconfig import S3_BUCKET_NAME


class GroupsState(rx.State):
    # Var containing a list of public groups and their group name, number of members, is user in group  # noqa: E501
    public_groups_displayed: list[tuple[Group, str, int, bool]] = []
    # Var containing a list of user's group and their group, group name, number of members  # noqa: E501
    user_groups_displayed: list[tuple[Group, str, int]] = []
    interests_names: list[str] = []

    group_interests: list[Interest] = []
    current_group_interest: int = 0

    new_group_image: str = ""
    new_group_name: str = ""
    new_group_interest_name: list[str] = []

    async def init(self):
        self.new_group_image: str = "blank_group_image"
        self.new_group_name: str = ""
        self.new_group_interest_name: list[str] = []

        await self.load_groups()

    async def load_groups(self, interest_id: int = 0):
        self.user_groups_displayed = []  # Groups the user is part of
        self.group_interests = []  # Interests of the groups to filter
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
            self.group_interests.append(group.interest)

        # Keep only groups with the selected interest
        if interest_id != 0:
            public_groups = [
                group for group in public_groups if group.interest_id == interest_id  # noqa: E501
            ]

        for group in public_groups:
            self.public_groups_displayed.append(
                (group,
                 Group.from_url_name(group.name),
                 len(group.user_group_list),                            # Number of members  # noqa: E501
                 (group.id in [group.id for group in user_groups]))     # Check if the current group is in the user's groups  # noqa: E501
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

    def set_current_group_interest(self, interest: Interest):
        self.current_group_interest = interest['id']
        return GroupsState.load_groups(interest['id'])

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
                    group_interest_filter(
                        group_interests=GroupsState.group_interests,
                        current_badge=GroupsState.current_group_interest,
                        on_change=GroupsState.set_current_group_interest,
                    ),

                    # Dialog to create a new group
                    new_group_dialog(),

                    justify='between',
                    style=rx.Style(
                        align_items='start',
                        margin_bottom='1em',
                        width='100%',
                    ),
                ),
                rx.tablet_and_desktop(
                    public_groups_grid(),
                ),
                rx.mobile_only(
                    public_groups_grid(column_nb='1'),
                ),
                style=rx.Style(
                    align_items='center',
                    background_color='white',
                    height='100%',
                    padding='2em',
                    border_radius='1.5em',
                    width=['100%', '100%', '100%', '76%'],
                ),
            ),
            rx.desktop_only(
                rx.vstack(
                    rx.text(
                        "Mes Fratries",
                        style=rx.Style(
                            font_size='1.5em',
                            font_weight='700'
                        ),
                    ),
                    rx.grid(
                        rx.foreach(
                            GroupsState.user_groups_displayed,
                            lambda group: rx.card(
                                rx.box(
                                    rx.hstack(
                                        rx.text(
                                            group[1],
                                            style=rx.Style(
                                                font_size='1em',
                                                font_weight='600',
                                                overflow='hidden',
                                                text_overflow='ellipsis',
                                                white_space='nowrap',
                                            ),
                                        ),
                                        interest_chip(group[0].interest),
                                        justify='between',
                                        width='100%',
                                    ),
                                    rx.text(
                                        f"{group[2]}/"
                                        f"{group[0].max_members} membres",
                                        style=rx.Style(
                                            color='gray',
                                            font_size='0.8em',
                                            margin_top='0.5em'
                                        )
                                    ),
                                    width='100%'
                                ),
                                cursor='pointer',
                                on_click=rx.redirect(
                                    f"{GROUPS_ROUTE}/{group[0].name}"
                                ),
                                style=rx.Style(
                                    width='100%',
                                    _hover={
                                        'box_shadow': '0px 1px 2px 1px rgba(0, 0, 0, 0.2)',  # noqa: E501
                                    }
                                ),
                            ),
                        ),
                        columns='1',
                        spacing='2',
                        width='100%'
                    ),
                    justify='start',
                    style=rx.Style(
                        background_color='white',
                        padding='1em 2em 1.5em',
                        border_radius='1.5em',  # solid #e5e5e5
                    ),
                ),
                width='24%',
            ),
            align_items='start',
            spacing='7',
        )
    )
