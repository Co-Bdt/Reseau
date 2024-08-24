import reflex as rx
from typing import Callable, List
from ..models import UserPrivateMessage, UserAccount


def private_discussion(
    authenticated_user: UserAccount,
    other_user: UserAccount,
    messages: List[UserPrivateMessage],
    send_message: Callable,
):
    """
    A component to display a private discussion with another user.

    Args:
        authenticated_user: The UserAccount of the authenticated user.
        other_user: The UserAccount of the other user in the conversation.
        messages: A list of PrivateMessage objects.
        send_message: A function to send a message to the other user.
    """
    return rx.vstack(
        rx.box(
            rx.foreach(
                messages,
                lambda msg: message_bubble(msg, authenticated_user)
            ),
        ),
        rx.separator(),
        rx.form(
            rx.hstack(
                rx.input(
                    name="message",
                    placeholder=f"Ecris à {other_user.first_name}",
                ),
                rx.input(
                    name="recipient_id",
                    value=other_user.id,
                    style=rx.Style(display="none"),
                ),
                rx.button("Send", type="submit"),
            ),
            on_submit=send_message,
            reset_on_submit=True,
        ),
        width="100%",
    )


def message_bubble(
    message: UserPrivateMessage,
    authenticated_user: UserAccount
):
    """
    A component to display a single message in a bubble.

    Args:
        message: A PrivateMessage object.
    """
    return rx.box(
        rx.text(message.private_message.content),
        padding="2",
        border="1px solid #eaeaea",
        border_radius="lg",
        background_color=rx.cond(
            message.sender_id == authenticated_user.id,
            "#F9F8F8",
            "#FFC53D"
        ),
        align_self="flex-start",
    )
