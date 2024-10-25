import reflex as rx

from .common.private_discussion import private_discussion
from ..components.profile_picture import profile_picture
from ..models import UserAccount, City
from ..pages.private_discussions import PrivateDiscussionsState


def user_hover_card(user: UserAccount, city: City) -> rx.Component:
    return rx.hstack(
        profile_picture(
            style=rx.Style(
                width='5.5em',
                height='5.5em',
            ),
            profile_picture=user.profile_picture,
        ),
        rx.vstack(
            rx.text(
                f"{user.first_name} {user.last_name}",
                style=rx.Style(
                    font_family='Inter, sans-serif',
                    font_weight='500',
                ),
            ),
            rx.text(
                f"{city.name} ({city.postal_code})",
                margin_bottom='0.5em',
                style=rx.Style(
                    color='gray',
                    font_family='Inter, sans-serif',
                    font_size='0.8em',
                ),
            ),
            rx.hstack(
                rx.dialog.root(
                    rx.dialog.trigger(
                        rx.button(
                            rx.text(
                                "Discussion",
                                font_family='Inter, sans-serif'
                            ),
                            on_click=PrivateDiscussionsState.load_private_messages(  # noqa: E501
                                user.id,
                            ),
                        ),
                    ),
                    rx.dialog.content(
                        rx.dialog.title(
                            rx.hstack(
                                profile_picture(
                                    style=rx.Style(
                                        width=['2.5em', '2.5em', '2.5em', '2.1em'],  # noqa: E501
                                        height=['2.5em', '2.5em', '2.5em', '2.1em'],  # noqa: E501
                                    ),
                                    profile_picture=user.profile_picture
                                ),
                                rx.text(
                                    f"{user.first_name} "
                                    f"{user.last_name}",
                                    font_family='Inter, sans-serif',
                                ),
                            ),
                        ),
                        private_discussion(
                            messages=PrivateDiscussionsState.discussion_messages,  # noqa: E501
                            # recipient=user,
                        ),
                        rx.form(
                            rx.hstack(
                                rx.input(
                                    name='recipient_id',
                                    value=user.id,
                                    style=rx.Style(display='none'),
                                ),
                                rx.input(
                                    name='message',
                                    placeholder=f"Écris à {user.first_name}",
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
                    ),
                ),
                justify='end',
            ),
            spacing='1',
        ),
    ),
