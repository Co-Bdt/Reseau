from datetime import datetime, timezone
from itertools import groupby
import os
import time
import boto3
import reflex as rx
import sqlalchemy as sa

from reseau.components.profile_picture import profile_picture
from reseau.components.user_hover_card import user_hover_card

from ..common.base_state import BaseState
from ..common.template import template
from ..common.translate import format_to_date
from ..components.custom.autosize import autosize_textarea
from ..components.group.dropdown_menu import dropdown_menu
from ..components.common.private_discussion import private_discussion
from ..models import Group, GroupMessage, Message, UserAccount, UserGroup
from ..reseau import GROUPS_ROUTE
from rxconfig import S3_BUCKET_NAME


class GroupState(rx.State):
    group: Group = None
    image: str = ''
    group_details: tuple[str, int] = ('', 0)

    is_current_user_owner: bool = False
    user_groups: list[UserGroup] = []
    group_messages: list[tuple[list[Message], str]] = []

    members_before_rm: list[UserGroup] = []

    message_content: str = ''

    async def init(self):
        base_state = await self.get_state(BaseState)

        with rx.session() as session:
            group = session.exec(
                Group.select()
                .options(
                    sa.orm.selectinload(Group.interest),
                    sa.orm.selectinload(Group.user_group_list)
                    .selectinload(UserGroup.useraccount)
                    .selectinload(UserAccount.city),
                    sa.orm.selectinload(Group.group_message_list)
                    .selectinload(GroupMessage.message)
                    .selectinload(Message.sender),
                )
                .where(Group.name == self.name)
            ).first()
        self.group = group
        if self.group.image:
            self.image = self.group.image
        else:
            self.image = "blank_group_image"

        self.group_details = (
            Group.from_url_name(self.name),
            len(group.user_group_list)
        )
        self.user_groups = group.user_group_list

        # Check if the current user is the owner of the group
        self.is_current_user_owner = any(
            user_group.is_owner
            for user_group in self.user_groups
            if user_group.useraccount_id == base_state.authenticated_user.id
        )

        # Load the group messages
        self.load_discussion(group.group_message_list)

    def load_discussion(self, group_messages: list[GroupMessage]):
        messages = [
            group_message.message
            for group_message in group_messages
        ]

        # Convert all published_at to Paris time
        os.environ['TZ'] = 'Europe/Paris'
        time.tzset()
        for message in messages:
            paris_now = datetime.now().timestamp()
            offset = (datetime.fromtimestamp(paris_now) -
                      datetime.utcfromtimestamp(paris_now))
            message.published_at = (
                message.published_at + offset
            )

        messages = sorted(
            messages,
            key=lambda x: x.published_at
        )

        # Function with which we group the messages by date
        def get_date(message: Message):
            return message.published_at.date()

        self.group_messages = [
            (list(group), format_to_date(date))
            for date, group in groupby(messages, key=get_date)
        ]

    def handle_dialog_open(self):
        self.members_before_rm = self.user_groups.copy()

    def mark_member_to_remove(self, user_group: UserGroup):
        self.members_before_rm.remove(user_group)

    async def remove_members(self):
        with rx.session() as session:
            for user_group in self.user_groups:
                if user_group not in self.members_before_rm:
                    session.delete(user_group)
            session.commit()
        await self.init()
        return

    async def handle_upload(self, files: list[rx.UploadFile]):
        '''Handle the upload of file(s).

        Args:
            files: The uploaded file(s).
        '''
        file = files[0]

        # Read uploaded file and prepare to save it
        upload_data = await file.read()
        outfile = (
            rx.get_upload_dir() /
            f"group_{self.group.id}" /
            file.filename
        )

        # # Create the group's directory if it doesn't exist
        # Path(
        #     rx.get_upload_dir() /
        #     f"group_{self.group.id}"
        # ).mkdir(parents=True, exist_ok=True)

        # Save the file
        with outfile.open('wb') as file_object:
            file_object.write(upload_data)

        # Update the group_image var
        self.image = (
            f"group_{self.group.id}/" +
            f"{file.filename}"
        )

    def edit_group(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)

        # Upload the profile picture to S3
        try:
            bucket.upload_file(
                rx.get_upload_dir() / self.image,
                self.image,
            )
        except Exception:
            return

        # Apply the changes to the group
        try:
            with rx.session() as session:
                current_group = session.exec(
                    Group.select()
                    .where(Group.id == self.group.id)
                ).first()
                current_group.image = self.image
                session.add(current_group)
                session.commit()
        except Exception:
            self.profile_pic = "blank_profile_picture"
            return
        return rx.toast.success("Fratrie mise à jour.")

    async def quit_group(self):
        base_state = await self.get_state(BaseState)

        with rx.session() as session:
            user_group = session.exec(
                UserGroup.select()
                .where(
                    UserGroup.useraccount_id ==
                    base_state.authenticated_user.id
                )
                .where(UserGroup.group_id == self.group.id)
            ).first()
            session.delete(user_group)
            session.commit()
        return rx.redirect(GROUPS_ROUTE)

    def delete_group(self):
        with rx.session() as session:
            # Delete all usergroups in the group
            user_groups = session.exec(
                UserGroup.select()
                .where(UserGroup.group_id == self.group.id)
            ).all()
            for user_group in user_groups:
                session.delete(user_group)

            # Delete all messages in the group
            group_messages = session.exec(
                GroupMessage.select()
                .where(GroupMessage.group_id == self.group.id)
            ).all()
            for group_message in group_messages:
                message = session.exec(
                    Message.select()
                    .where(Message.id == group_message.message_id)
                ).first()
                session.delete(message)
                session.delete(group_message)

            # Delete the group
            session.delete(self.group)
            session.commit()
        return rx.redirect(GROUPS_ROUTE)

    async def send_message(self, form_data: dict):
        base_state = await self.get_state(BaseState)

        if not form_data['message']:
            return

        with rx.session() as session:
            new_message = Message(
                content=form_data['message'],
                published_at=datetime.now(timezone.utc),
                sender_id=base_state.authenticated_user.id
            )
            session.add(new_message)
            session.commit()
            session.refresh(new_message)

            group_message = GroupMessage(
                group_id=self.group.id,
                message_id=new_message.id,
            )
            session.add(group_message)
            session.commit()
        # TODO:
        # Notify group members of new messages
        await self.init()
        return


@rx.page(
    title="Fratries",
    route=f'{GROUPS_ROUTE}/[name]',
    on_load=GroupState.init
)
@template
def group_page():
    return rx.cond(
        GroupState.is_hydrated,
        rx.cond(
            GroupState.group,
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        # rx.image(
                        #     src=rx.get_upload_url(
                        #         GroupState.image
                        #     ),
                        #     width=['5em'],
                        #     height=['5em'],
                        #     border_radius='50%',
                        #     object_fit="cover",
                        # ),
                        rx.hstack(
                            profile_picture(
                                style=rx.Style(
                                    width='5em',
                                    height='5em',
                                ),
                                profile_picture=GroupState.image,
                            ),
                            rx.vstack(
                                rx.text(
                                    GroupState.group_details[0],
                                    style=rx.Style(
                                        font_size='1.75em',
                                        font_weight='600'
                                    )
                                ),
                                rx.text(
                                    f"{GroupState.group_details[1]}/"
                                    f"{GroupState.group.max_members} membres",
                                    style=rx.Style(
                                        color='gray',
                                        font_size='0.8em',
                                    )
                                ),
                                spacing='1'
                            ),
                            align='start'
                        ),
                        # Dropdown menu with group actions
                        dropdown_menu(),
                        justify='between',
                        width='100%'
                    ),
                    # Messages
                    private_discussion(
                        messages=GroupState.group_messages,
                        is_group_discussion=True,
                    ),
                    # Text input
                    rx.form(
                        rx.hstack(
                            rx.input(
                            #     auto_complete=False,
                            #     name='message',
                                on_change=GroupState.set_message_content,
                                display='none',
                            #     placeholder=(
                            #         f"Écris dans {GroupState.group_details[0]}"
                            #     ),
                            #     size='2',
                            #     value=GroupState.message_content,
                            #     style=rx.Style(
                            #         font_family='Inter, sans-serif',
                            #         width='100%',
                            #     ),
                            ),
                            autosize_textarea(
                                class_name='autosize-group-message',
                                id='message',
                                value=GroupState.message_content,
                            ),
                            rx.icon_button(
                                rx.icon('send-horizontal', size=24),
                                size='3', type='submit', variant='soft',
                                # disabled=~GroupState.message_content,
                                style=rx.Style(
                                    background='transparent',
                                    _hover={
                                        'bg': rx.color('gray', 4),
                                    },
                                    # color='white',
                                    # height='100%',
                                    # width='3em',
                                    cursor='pointer',
                                ),
                            ),
                            width='100%',
                        ),
                        auto_complete='off',
                        on_submit=GroupState.send_message,
                        reset_on_submit=True,
                    ),
                    style=rx.Style(
                        background_color='white',
                        height='100%',
                        padding='1em 2em 2em',
                        border_radius='1.5em',  # solid #e5e5e5
                        width='76%',
                    ),
                ),
                rx.vstack(
                    rx.text(
                        "Membres",
                        style=rx.Style(
                            font_size='1.5em',
                            font_weight='600'
                        )
                    ),
                    rx.grid(
                        rx.foreach(
                            GroupState.user_groups,
                            lambda user_group: rx.card(
                                rx.hstack(
                                    rx.hover_card.root(
                                        rx.hover_card.trigger(
                                            rx.link(
                                                rx.text(
                                                    f"{user_group.useraccount.first_name} "  # noqa: E501
                                                    f"{user_group.useraccount.last_name}",  # noqa: E501
                                                ),
                                                color='inherit',
                                                cursor='default',
                                            ),
                                        ),
                                        rx.hover_card.content(
                                            user_hover_card(
                                                user_group.useraccount,
                                                user_group.useraccount.city,
                                            ),
                                        ),
                                    ),
                                    rx.cond(
                                        user_group.is_owner,
                                        rx.icon('crown', size=20),
                                    ),
                                    justify='between',
                                    width='100%'
                                ),
                                width='100%'
                            ),
                        ),
                        columns='1',
                        spacing='2',
                        width='100%'
                    ),
                    style=rx.Style(
                        background_color='white',
                        padding='1em 2em 1.5em',
                        border_radius='1.5em',  # solid #e5e5e5
                        width='24%',
                    ),
                ),
                align_items='start',
                spacing='7',
                height='100%',
            ),
            rx.text("Fratrie non trouvée")
        )
    )
