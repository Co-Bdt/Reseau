import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..components.private_discussion import private_discussion
from ..models import UserAccount, UserPrivateMessage
from ..reseau import PRIVATE_DISCUSSIONS_ROUTE


class PrivateDiscussionsState(BaseState):
    """State for managing private messages."""

    # A collection of discussions, each one containing 
    # the UserAccount to which the current User talks to
    # and all the private messages between them
    private_discussions: list[UserAccount] = []
    discussion_messages: list[UserPrivateMessage] = []

    def load_private_discussions(self):
        """
        Load private discussions for the current user.
        """
        with rx.session() as session:
            user = session.exec(
                UserAccount.select()
                .options(
                    sa.orm.selectinload(
                        UserAccount.user_private_message_sent_list
                    ).selectinload(UserPrivateMessage.private_message),
                    sa.orm.selectinload(
                        UserAccount.user_private_message_sent_list
                    ).selectinload(UserPrivateMessage.sender),
                    sa.orm.selectinload(
                        UserAccount.user_private_message_sent_list
                    ).selectinload(UserPrivateMessage.recipient),
                    sa.orm.selectinload(
                        UserAccount.user_private_message_received_list
                    ).selectinload(UserPrivateMessage.sender),
                    sa.orm.selectinload(
                        UserAccount.user_private_message_received_list
                    ).selectinload(UserPrivateMessage.recipient),
                    sa.orm.selectinload(
                        UserAccount.user_private_message_received_list
                    ).selectinload(UserPrivateMessage.private_message)
                ).where(
                    UserAccount.id == self.authenticated_user.id
                )
            ).first()

        for pm in user.user_private_message_sent_list:
            print("pm sender: ", pm.sender.id)
            print("pm recipient: ", pm.recipient.id)

            if pm.recipient not in self.private_discussions:
                self.private_discussions.append(pm.recipient)

    def load_private_messages(self, discussion_id: int):
        """
        Load private messages for a discussion.
        """
        print(f"Loading private messages for discussion {discussion_id}")
        with rx.session() as session:
            messages = session.exec(
                UserPrivateMessage.select()
                .options(
                    sa.orm.selectinload(UserPrivateMessage.private_message)
                ).where(
                    ((UserPrivateMessage.sender_id == self.authenticated_user.id) &
                        (UserPrivateMessage.recipient_id == discussion_id)) |
                    ((UserPrivateMessage.recipient_id == self.authenticated_user.id) &
                        (UserPrivateMessage.sender_id == discussion_id))
                )
            ).all()
            print(f"messages: {messages}")
            self.discussion_messages = messages


@rx.page(
    title="Reseau",
    route=PRIVATE_DISCUSSIONS_ROUTE,
    on_load=PrivateDiscussionsState.load_private_discussions
)
@template
def private_messages():
    """
    Page component to display private message discussions.
    """
    return rx.vstack(
        rx.heading("Messages privés", size="lg"),
        rx.box(
            rx.foreach(
                PrivateDiscussionsState.private_discussions,
                lambda discussion: rx.dialog.root(
                    rx.dialog.trigger(
                        rx.button(
                            rx.text(f"Discussion avec {discussion.first_name} {discussion.last_name}"),
                            on_click=PrivateDiscussionsState.load_private_messages(discussion.id),
                            as_child=True
                        ),
                    ),
                    rx.dialog.content(
                        rx.dialog.title(
                            rx.text(f"{discussion.first_name} {discussion.last_name}"),
                        ),
                        private_discussion(
                            messages=PrivateDiscussionsState.discussion_messages,
                            other_user=discussion
                        )
                    )
                )
            ),
        ),
        width="100%",
    )
