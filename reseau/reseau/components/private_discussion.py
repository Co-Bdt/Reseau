import reflex as rx
from typing import Callable, List

from ..common.base_state import BaseState

from reseau.components.profile_picture import profile_picture
from ..models import UserPrivateMessage, UserAccount


common_style = rx.Style(
    max_width='80%',
    padding='0.8em',
    border='0.5px solid #eaeaea',
    border_radius='1em',
    box_shadow='0px 2px 2px rgba(0, 0, 0, 0.15)',
)


def private_discussion(
    other_user: UserAccount,
    messages: List[UserPrivateMessage],
    send_message: Callable,
):
    '''
    A component to display a private discussion with another user.

    Args:
        authenticated_user: The UserAccount of the authenticated user.
        other_user: The UserAccount of the other user in the conversation.
        messages: A list of PrivateMessage objects.
        send_message: A function to send a message to the other user.
    '''
    return rx.vstack(
        rx.separator(
            margin_y='0.5em',
        ),
        rx.vstack(
            rx.cond(
                messages,
                rx.flex(
                    rx.foreach(
                        messages,
                        lambda msg: message_bubble(msg)
                    ),
                    direction='column',
                    width='100%',
                    spacing='0.8em',
                ),
                rx.hstack(
                    rx.text(
                        "Tu es sur le point de briser la glace !",
                        color='gray',
                        font_size='0.9em',
                    ),
                    width='100%',
                    justify='center',
                ),
            ),
            rx.separator(
                margin_y='0.5em',
            ),
            rx.form(
                rx.hstack(
                    rx.input(
                        name='recipient_id',
                        value=other_user.id,
                        style=rx.Style(display='none'),
                    ),
                    rx.box(
                        rx.tablet_and_desktop(
                            rx.input(
                                name='message',
                                placeholder=f"Écris à {other_user.first_name}",
                                size='3',
                            ),
                        ),
                        rx.mobile_only(
                            rx.input(
                                name='message',
                                placeholder=f"Écris à {other_user.first_name}",
                                size='2',
                            ),
                        ),
                        width='100%',
                    ),
                    rx.tablet_and_desktop(
                        rx.button("Envoyer", type='submit', size='3'),
                    ),
                    rx.mobile_only(
                        rx.button("Envoyer", type='submit', size='2'),
                    ),
                    width='100%',
                ),
                on_submit=send_message,
                reset_on_submit=True,
            ),
            width='100%',
        ),
        width='100%',
        justify='between',
    )


def message_bubble(
    message: UserPrivateMessage
):
    '''
    A component to display a single message in a bubble.

    Args:
        message: A PrivateMessage object.
    '''
    return rx.cond(
        message.sender_id == BaseState.authenticated_user.id,
        rx.hstack(
            rx.box(
                rx.text(
                    message.private_message.content,
                    font_size=['0.9em', '0.9em', '0.9em', '1em'],
                ),
                background_color=rx.color_mode_cond(
                    light='#F9F8F8',
                    dark='#121212',
                ),
                style=common_style,
            ),
            profile_picture(
                style=rx.Style(
                    width=['2.5em', '2.5em', '2.5em', '2.7em'],  # noqa
                    height=['2.5em', '2.5em', '2.5em', '2.7em'],  # noqa
                ),
                profile_picture=message.sender.profile_picture
            ),
            justify='end',
            align_items='start',
        ),
        rx.hstack(
            profile_picture(
                style=rx.Style(
                    width=['2.5em', '2.5em', '2.5em', '2.7em'],  # noqa
                    height=['2.5em', '2.5em', '2.5em', '2.7em'],  # noqa
                ),
                profile_picture=message.sender.profile_picture
            ),
            rx.box(
                rx.text(
                    message.private_message.content,
                    font_size=['0.9em', '0.9em', '0.9em', '1em'],
                ),
                background_color=rx.color_mode_cond(
                    light='#FFF6E0',
                    dark='#36290D',
                ),
                style=common_style,
            ),
            align_items='start',
        ),
    )
