import reflex as rx

from reseau.components.common.private_discussion import private_discussion

from ..pages.private_discussions import PrivateDiscussionsState
from .profile_picture import profile_picture


item_style = rx.Style(
    cursor='pointer',
    align='center',
    padding='6px',
    border_radius='0.5em',
    _hover={
        'bg': rx.color('gray', 4),
    },
)


def private_discussions_popover():
    return rx.popover.root(
        rx.popover.trigger(
            rx.box(
                rx.desktop_only(
                    rx.hstack(
                        rx.color_mode_cond(
                            light=rx.icon('message-square', color='black', size=28),  # noqa: E501
                            dark=rx.icon('message-square', color='white', size=28),  # noqa: E501
                        ),
                        style=item_style,
                    ),
                ),
                rx.mobile_and_tablet(
                    rx.hstack(
                        rx.color_mode_cond(
                            light=rx.icon('message-square', color='black', size=24),  # noqa: E501
                            dark=rx.icon('message-square', color='white', size=24),  # noqa: E501
                        ),
                        style=item_style,
                    ),
                ),
                rx.cond(
                    PrivateDiscussionsState.is_there_unread_messages,
                    rx.box(
                        width="0.7em",
                        height="0.7em",
                        background_color="#192bc2",
                        border_radius="50%",
                        position="absolute",
                        bottom="0.35em",
                        right="0.35em",
                        transform="translate(50%, 50%)",
                    ),
                ),
                position="relative",
            ),
        ),
        rx.popover.content(
            rx.text(
                "Discussions",
                style=rx.Style(
                    font_family='Inter, sans-serif',
                    font_weight='500',
                    margin_bottom='0.5em',
                ),
            ),
            rx.cond(
                PrivateDiscussionsState.private_discussions,
                rx.foreach(
                    PrivateDiscussionsState.private_discussions,
                    lambda discussion: rx.dialog.root(
                        rx.dialog.trigger(
                            rx.card(
                                rx.hstack(
                                    rx.hstack(
                                        profile_picture(
                                            style=rx.Style(
                                                width=['1.8em', '1.8em', '1.8em', '2em'],  # noqa
                                                height=['1.8em', '1.8em', '1.8em', '2em'],  # noqa
                                                filter=rx.cond(
                                                    ~discussion[1],
                                                    'none',
                                                    'opacity(40%)',
                                                )
                                            ),
                                            profile_picture=discussion[0].profile_picture  # noqa
                                        ),
                                        rx.text(
                                            f"{discussion[0].first_name} "
                                            f"{discussion[0].last_name}",
                                            style=rx.Style(
                                                color=rx.cond(
                                                    discussion[1],
                                                    'gray',
                                                    'black',
                                                ),
                                                font_family=('Inter, '
                                                             'sans-serif'),
                                                font_weight='500',
                                            ),
                                        ),
                                    ),
                                    rx.cond(
                                        ~discussion[1],
                                        rx.icon(
                                            'dot',
                                            color='#192bc2',
                                            size=64,
                                            margin='-1em',
                                        ),
                                    ),
                                    justify='between',
                                    padding='0.3em',
                                ),
                                cursor='pointer',
                                min_width='20em',
                            ),
                            on_click=PrivateDiscussionsState.load_private_messages(  # noqa
                                discussion[0].id,
                                True
                            ),
                            margin_top='0.5em',
                        ),
                        rx.dialog.content(
                            rx.dialog.title(
                                rx.hstack(
                                    profile_picture(
                                        style=rx.Style(
                                            width=['2.5em', '2.5em', '2.5em', '2.1em'],  # noqa
                                            height=['2.5em', '2.5em', '2.5em', '2.1em'],  # noqa
                                        ),
                                        profile_picture=discussion[0].profile_picture  # noqa
                                    ),
                                    rx.text(
                                        f"{discussion[0].first_name} "
                                        f"{discussion[0].last_name}",
                                        font_family=('Inter, '
                                                     'sans-serif'),
                                    ),
                                ),
                                margin_top='0.5em',
                            ),
                            private_discussion(
                                messages=PrivateDiscussionsState.discussion_messages,  # noqa
                            ),
                            rx.form(
                                rx.hstack(
                                    rx.input(
                                        name='recipient_id',
                                        value=discussion[0].id,
                                        style=rx.Style(display='none'),
                                    ),
                                    rx.input(
                                        name='message',
                                        placeholder=(
                                            f"Écris à "
                                            f"{discussion[0].first_name}"
                                        ),
                                        size='3',
                                        style=rx.Style(
                                            font_family='Inter, sans-serif',
                                            width='100%',
                                        ),
                                    ),
                                    rx.button(
                                        rx.text(
                                            "Envoyer",
                                            font_family='Inter, sans-serif'
                                        ),
                                        type='submit', size='3'
                                    ),
                                    width='100%',
                                ),
                                on_submit=PrivateDiscussionsState.send_message,
                                reset_on_submit=True,
                            ),
                            max_height='75vh',
                            padding='1em',
                        )
                    ),
                ),
                rx.hstack(
                    rx.text(
                        "Démarre une discussion depuis la page des membres",
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
            padding='0.8em',
        ),
        on_open_change=PrivateDiscussionsState.load_private_discussions
    )
