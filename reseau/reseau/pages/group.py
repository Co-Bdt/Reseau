from datetime import datetime, timezone
import boto3
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..models import Group, GroupMessage, Message, UserGroup
from ..reseau import GROUPS_ROUTE
from rxconfig import S3_BUCKET_NAME


class GroupState(rx.State):
    group: Group = None
    image: str = ''
    group_details: tuple[str, int] = ('', 0)

    is_current_user_owner: bool = False
    user_groups: list[UserGroup] = []
    group_messages: list[GroupMessage] = []

    members_before_rm: list[UserGroup] = []

    async def init(self):
        base_state = await self.get_state(BaseState)

        with rx.session() as session:
            group = session.exec(
                Group.select()
                .options(
                    sa.orm.selectinload(Group.interest),
                    sa.orm.selectinload(Group.user_group_list)
                    .selectinload(UserGroup.useraccount),
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
        yield
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
        self.group_messages = group.group_message_list

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
                        rx.image(
                            src=rx.get_upload_url(
                                GroupState.image
                            ),
                            width=['5em'],
                            height=['5em'],
                            border_radius='50%',
                            object_fit="cover",
                        ),
                        rx.vstack(
                            rx.text(GroupState.group_details[0]),
                            rx.text(f"{GroupState.group_details[1]}/{GroupState.group.max_members} membres"),
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.icon_button(
                                    rx.icon('ellipsis'),
                                )
                            ),
                            rx.cond(
                                GroupState.is_current_user_owner,
                                rx.menu.content(
                                    rx.dialog.root(
                                        rx.dialog.trigger(
                                            rx.button(
                                                "Gérer les membres",
                                                on_click=GroupState.handle_dialog_open,
                                            )
                                        ),
                                        rx.dialog.content(
                                            rx.dialog.title("Gérer les membres"),
                                            rx.foreach(
                                                GroupState.members_before_rm,
                                                lambda member: rx.cond(
                                                    ~member.is_owner,
                                                    rx.card(
                                                        rx.text(
                                                            f"{member.useraccount.first_name} ",
                                                            f"{member.useraccount.last_name}"
                                                        ),
                                                        rx.icon_button(
                                                            rx.icon('x'),
                                                            on_click=GroupState.mark_member_to_remove(
                                                                member
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            rx.flex(
                                                rx.dialog.close(
                                                    rx.button(
                                                        "Annuler",
                                                        color_scheme="gray",
                                                        variant="soft",
                                                    ),
                                                ),
                                                rx.dialog.close(
                                                    rx.button(
                                                        "Valider",
                                                        on_click=GroupState.remove_members,
                                                    ),
                                                ),
                                                justify="end",
                                                spacing="3",
                                                margin_top="16px",
                                            ),
                                        ),
                                    ),
                                    rx.menu.separator(),
                                    rx.dialog.root(
                                        rx.dialog.trigger(
                                            rx.button("Modifier la Fratrie",)
                                        ),
                                        rx.dialog.content(
                                            rx.dialog.title("Modifier la Fratrie"),
                                            rx.upload(
                                                rx.image(
                                                    src=rx.get_upload_url(
                                                        GroupState.image
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
                                                on_drop=GroupState.handle_upload(
                                                    rx.upload_files(upload_id='group_img')
                                                ),
                                                padding='0',
                                                width='6em',
                                                height='5em',
                                                border='none',
                                            ),
                                            rx.flex(
                                                rx.dialog.close(
                                                    rx.button(
                                                        "Annuler",
                                                        color_scheme="gray",
                                                        variant="soft",
                                                    ),
                                                ),
                                                rx.dialog.close(
                                                    rx.button(
                                                        "Valider",
                                                        on_click=GroupState.edit_group,
                                                    ),
                                                ),
                                                justify="end",
                                                spacing="3",
                                                margin_top="16px",
                                            ),
                                        ),
                                    ),
                                    rx.alert_dialog.root(
                                        rx.alert_dialog.trigger(
                                            rx.button("Dissoudre la Fratrie"),
                                        ),
                                        rx.alert_dialog.content(
                                            rx.alert_dialog.title("Dissoudre la Fratrie"),
                                            rx.alert_dialog.description(
                                                "Veux-tu vraiment dissoudre cette Fratrie ?\n"
                                                "Toutes les données seront perdues."
                                            ),
                                            rx.flex(
                                                rx.alert_dialog.cancel(
                                                    rx.button("Annuler"),
                                                ),
                                                rx.alert_dialog.action(
                                                    rx.button(
                                                        "Dissoudre",
                                                        on_click=GroupState.delete_group
                                                    ),
                                                ),
                                                justify='end',
                                                spacing='3',
                                            ),
                                        ),
                                    ),
                                ),
                                rx.menu.content(
                                    rx.menu.item(
                                        "Quitter la Fratrie",
                                        on_click=GroupState.quit_group,
                                    ),
                                ),
                            ),
                        ),
                        justify='space-between'
                    ),
                    # Messages
                    rx.flex(
                        rx.foreach(
                            GroupState.group_messages,
                            lambda msg: rx.card(
                                rx.text(
                                    f"{msg.message.sender.first_name} ",
                                    f"{msg.message.sender.last_name}"
                                ),
                                rx.text(msg.message.content)
                            )
                        ),
                        direction='column',
                    ),
                    # Text input
                    rx.form(
                        rx.hstack(
                            rx.input(
                                name='message',
                                placeholder=f"Écris dans {GroupState.group_details[0]}",
                                size='3',
                                style=rx.Style(
                                    font_family='Inter, sans-serif',
                                    width='100%',
                                ),
                            ),
                            rx.icon_button(
                                rx.icon('send-horizontal'),
                                type='submit', size='3'
                            ),
                            width='100%',
                        ),
                        on_submit=GroupState.send_message,
                        reset_on_submit=True,
                    ),
                    width='85%',
                ),
                rx.vstack(
                    rx.text("Membres"),
                    rx.grid(
                        rx.foreach(
                            GroupState.user_groups,
                            lambda user_group: rx.card(
                                rx.hstack(
                                    rx.text(
                                        f"{user_group.useraccount.first_name} ",
                                        f"{user_group.useraccount.last_name}"
                                    ),
                                    rx.cond(
                                        user_group.is_owner,
                                        rx.icon('crown'),
                                    ),
                                ),
                            ),
                        ),
                        columns='1'
                    ),
                    width='15%'
                ),
            ),
            rx.text("Fratrie non trouvée")
        )
    )
