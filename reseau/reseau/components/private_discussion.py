import reflex as rx

from ..common.base_state import BaseState
from ..components.profile_picture import profile_picture
from ..models import Message


common_style = rx.Style(
    max_width='80%',
    padding='0.6em 0.8em',
    border='0.5px solid #eaeaea',
    border_radius='0.5em',
    box_shadow='0px 2px 2px rgba(0, 0, 0, 0.15)',
)


def private_discussion(
    messages: list[tuple[list[Message], str]],
):
    '''
    A component to display a private discussion with another user.

    Args:
        other_user: The UserAccount of the other user in the conversation.
        messages: A list of PrivateMessage objects.
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
                        lambda msg: message_group(msg)
                    ),
                    direction='column',
                    width='100%',
                    spacing='0.8em',
                ),
                rx.hstack(
                    rx.text(
                        "Tu es sur le point de briser la glace !",
                        style=rx.Style(
                            color='gray',
                            font_family='Inter, sans-serif',
                            font_size='0.9em',
                        ),
                    ),
                    width='100%',
                    justify='center',
                ),
            ),
            rx.spacer(
                margin_bottom='0.75em',
            ),
            width='100%',
        ),
        style=rx.Style(
            height='60dvh',
            overflow_y='auto',
            width='100%',
        ),
    )


def message_group(
    messages: tuple[list[Message], str]
):
    '''
    A component to display a group of messages.

    Args:
        messages: A list of UserPrivateMessage objects.
    '''
    return rx.vstack(
        rx.hstack(
            rx.text(
                messages[1],
                style=rx.Style(
                    text_align='center',
                    color='gray',
                    font_size='0.8em',
                    font_family='Inter, sans-serif',
                ),
            ),
            width='100%',
            justify='center',
        ),
        rx.foreach(
            messages[0],
            lambda message: message_bubble(message),
        ),
        width='100%',
        margin_bottom='0.5em',
    )


def message_bubble(
    # message: UserPrivateMessage
    message: Message
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
                rx.hstack(
                    rx.text(
                        message.content,
                        style=rx.Style(
                            font_family='Inter, sans-serif',
                            font_size=['0.9em', '0.9em', '0.9em', '1em'],
                        ),
                    ),
                    rx.text(
                        rx.moment(
                            message.published_at,
                            format='HH:mm'
                        ),
                        style=rx.Style(
                            color='gray',
                            font_family='Inter, sans-serif',
                            font_size='0.7em',
                        ),
                    ),
                    width='100%',
                    align_items='end',
                ),
                background_color='#F9F8F8',
                style=common_style,
            ),
            profile_picture(
                style=rx.Style(
                    width=['2.5em', '2.5em', '2.5em', '2.7em'],  # noqa
                    height=['2.5em', '2.5em', '2.5em', '2.7em'],  # noqa
                ),
                profile_picture=message.sender.profile_picture
            ),
            width='100%',
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
                rx.hstack(
                    rx.text(
                        message.content,
                        style=rx.Style(
                            font_family='Inter, sans-serif',
                            font_size=['0.9em', '0.9em', '0.9em', '1em'],
                        ),
                    ),
                    rx.text(
                        rx.moment(
                            message.published_at,
                            format="HH:mm"
                        ),
                        style=rx.Style(
                            color='gray',
                            font_family='Inter, sans-serif',
                            font_size='0.7em',
                        ),
                    ),
                    align_items='end',
                ),
                background_color='#FFF6E0',
                style=common_style,
            ),
            align_items='start',
        ),
    )
