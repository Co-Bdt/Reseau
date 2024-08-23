import reflex as rx
from typing import List
from ..models import UserPrivateMessage, UserAccount


def private_discussion(
    messages: List[UserPrivateMessage],
    other_user: UserAccount,  # TODO: remove because it is already in the messages
):
    """
    A component to display a private discussion with another user.

    Args:
        messages: A list of PrivateMessage objects.
        other_user: The UserAccount of the other user in the conversation.
    """
    return rx.vstack(
        rx.box(
            rx.foreach(
                messages,
                lambda msg: message_bubble(msg)
            ),
        ),
        rx.separator(),
        rx.hstack(
            rx.input(
                placeholder=f"Ecris à {other_user.first_name}",
            ),
            rx.button("Send"),
        ),
        width="100%",
    )


def message_bubble(message: UserPrivateMessage):
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
            message.sender_id == 1,
            "white",
            "yellow"
        ),
        align_self="flex-start",
    )
