from datetime import datetime
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..components.private_discussion import private_discussion
from ..models import PrivateMessage, UserAccount, UserPrivateMessage
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
        Load existing private discussions for the current user.
        """
        print("load_private_discussions")
        self.private_discussions = []

        with rx.session() as session:
            user = session.exec(
                UserAccount.select()
                .options(
                    sa.orm.selectinload(
                        UserAccount.user_private_message_sent_list
                    ).selectinload(UserPrivateMessage.recipient),
                    sa.orm.selectinload(
                        UserAccount.user_private_message_received_list
                    ).selectinload(UserPrivateMessage.sender),
                ).where(
                    UserAccount.id == self.authenticated_user.id
                )
            ).first()

        for pm in user.user_private_message_sent_list:
            if pm.recipient not in self.private_discussions:
                self.private_discussions.append(pm.recipient)

        for pm in user.user_private_message_received_list:
            if pm.sender not in self.private_discussions:
                self.private_discussions.append(pm.sender)

        print("private_discussions", self.private_discussions)

    def load_private_messages(self, discussion_id: int):
        """
        Load private messages for a discussion.
        """
        self.discussion_messages = []

        with rx.session() as session:
            messages = session.exec(
                UserPrivateMessage.select()
                .options(
                    sa.orm.selectinload(UserPrivateMessage.private_message),
                    sa.orm.selectinload(UserPrivateMessage.sender),
                    sa.orm.selectinload(UserPrivateMessage.recipient),
                ).where(
                    ((UserPrivateMessage.sender_id ==
                      self.authenticated_user.id) &
                     (UserPrivateMessage.recipient_id == discussion_id)) |
                    ((UserPrivateMessage.recipient_id ==
                      self.authenticated_user.id) &
                     (UserPrivateMessage.sender_id == discussion_id))
                )
            ).all()
            messages = sorted(
                messages,
                key=lambda x: x.private_message.published_at
            )
            self.discussion_messages = messages

        return rx.call_script(
            """
            console.log("load_private_messages event", event)
            """
        )

    def send_message(self, form_data: dict):
        """
        Send a message to a discussion.
        """
        with rx.session() as session:
            new_message = PrivateMessage(
                content=form_data["message"],
                published_at=datetime.now(),
            )
            session.add(new_message)
            session.commit()
            session.refresh(new_message)

            user_private_message = UserPrivateMessage(
                sender_id=self.authenticated_user.id,
                recipient_id=form_data["recipient_id"],
                private_message_id=new_message.id,
            )
            session.add(user_private_message)
            session.commit()

            self.load_private_messages(form_data["recipient_id"])


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
        rx.heading("Messages privés"),
        rx.box(
            rx.foreach(
                PrivateDiscussionsState.private_discussions,
                lambda discussion: rx.dialog.root(
                    rx.dialog.trigger(
                        rx.button(
                            rx.text(
                                f"Discussion avec {discussion.first_name} "
                                f"{discussion.last_name}"
                            ),
                            on_click=PrivateDiscussionsState.load_private_messages(  # noqa: E501
                                discussion.id
                            ),
                            as_child=True
                        ),
                    ),
                    rx.dialog.content(
                        rx.dialog.title(
                            rx.text(
                                f"{discussion.first_name} "
                                f"{discussion.last_name}"
                            ),
                        ),
                        private_discussion(
                            authenticated_user=PrivateDiscussionsState.authenticated_user,  # noqa: E501
                            other_user=discussion,
                            messages=PrivateDiscussionsState.discussion_messages,  # noqa: E501
                            send_message=PrivateDiscussionsState.send_message
                        )
                    )
                )
            ),
        ),
        width="100%",
    )
