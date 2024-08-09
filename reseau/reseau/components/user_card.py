import reflex as rx

from ..components.profile_picture import profile_picture
from ..models import City, Interest, UserAccount


class UserCard(rx.ComponentState):

    def interest_chip(interest: Interest) -> rx.Component:
        return rx.badge(
            interest.name,
            color_scheme="amber",
            radius="full",
            variant="surface",
        )

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        user: UserAccount = props.pop("user")
        city: City = props.pop("city")
        interest_list: list[Interest] = props.pop("interest_list", [])
        is_profile_empty = props.pop("is_profile_empty", True)

        return rx.card(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        profile_picture(
                            style=rx.Style(
                                width="2.7em",
                                height="2.7em",
                                border="0.5px solid #ccc",
                            ),
                            profile_picture=user.profile_picture,
                        ),
                        rx.vstack(
                            rx.text(
                                f"{user.username}",
                                size="2",
                                weight="medium",
                            ),
                            rx.text(
                                f"{city.name} ({city.postal_code})",
                                size="2",
                                color_scheme="gray",
                            ),
                            spacing="1",
                        ),
                        width="100%",
                        align="start",
                    ),
                    rx.hstack(
                        rx.foreach(
                            interest_list,
                            UserCard.interest_chip,
                        ),
                        spacing="1",
                    ),
                    rx.text(
                        f"{user.email}",
                        size="2",
                        color_scheme="gray",
                    ),
                    rx.box(
                        rx.cond(
                            is_profile_empty,
                            rx.text(
                                "Aucune description",
                                size="2",
                                color_scheme="gray",
                                style={
                                    "font-style": "italic",
                                },
                            ),
                            rx.text(
                                f"{user.profile_text}",
                                size="2",
                                style={
                                    "line-height": "1.4",
                                    "letter-spacing": "0.2px",
                                },
                            ),
                        ),
                        margin="0.5em 0 0 0"
                    ),
                ),
            ),
            as_child=True,
            size="3",
        )


user_card = UserCard.create
