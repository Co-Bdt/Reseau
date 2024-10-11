from datetime import datetime, timezone
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..models import Group, GroupMessage, Message, UserGroup
from ..reseau import GROUPS_ROUTE


class GroupState(rx.State):
    group: Group = None
    group_details: tuple[str, int] = ('', 0)
    user_groups: list[UserGroup] = []
    group_messages: list[GroupMessage] = []

    def init(self):
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
        self.group_details = (
            Group.from_url_name(self.name),
            len(group.user_group_list)
        )
        self.user_groups = group.user_group_list
        self.group_messages = group.group_message_list

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
        # Reload only the messages
        # Notify group members of new messages
        return self.init()


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
                            rx.menu.content(
                                rx.menu.item(
                                    "Quitter la Fratrie",
                                    on_click=GroupState.quit_group,
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
