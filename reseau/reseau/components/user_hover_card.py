import reflex as rx

from ..components.private_discussion import private_discussion
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
                style={
                    'font_weight': '500',
                },
            ),
            rx.text(
                f"{city.name} ({city.postal_code})",
                margin_bottom='0.5em',
                style={
                    'font_size': '0.8em',
                    'color': 'gray',
                },
            ),
            rx.hstack(
                rx.dialog.root(
                    rx.dialog.trigger(
                        rx.button(
                            "Discussion",
                            on_click=PrivateDiscussionsState.load_private_messages(  # noqa: E501
                                user.id,
                            ),
                        ),
                    ),
                    rx.dialog.content(
                        rx.dialog.title(
                            f"{user.first_name} {user.last_name}",
                        ),
                        private_discussion(
                            authenticated_user=PrivateDiscussionsState.authenticated_user,  # noqa: E501
                            other_user=user,
                            messages=PrivateDiscussionsState.discussion_messages,  # noqa: E501
                            send_message=PrivateDiscussionsState.send_message
                        )
                    ),
                ),
                justify='end',
            ),
            spacing='1',
        ),
    ),
