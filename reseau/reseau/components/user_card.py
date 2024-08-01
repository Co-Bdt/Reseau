from typing import Tuple
import reflex as rx

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
        user: Tuple[UserAccount, bool] = props.pop("user")
        city: City = props.pop("city")
        interest_list: list[Interest] = props.pop("interest_list", [])
        is_profile_empty = props.pop("is_profile_empty", True)

        return rx.card(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.cond(
                            user[1],
                            rx.image(
                                src=rx.get_upload_url(
                                    f"{user[0].id}_profile_picture.png"
                                ),
                                width="4.5vh",
                                height="4.5vh",
                                border="0.5px solid #ccc",
                                border_radius="50%",
                            ),
                            rx.image(
                                src=rx.get_upload_url(
                                    "blank_profile_picture.png"
                                ),
                                width="4.5vh",
                                height="4.5vh",
                                border="0.5px solid #ccc",
                                border_radius="50%",
                            ),
                        ),
                        rx.vstack(
                            rx.text(
                                f"{user[0].username}",
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
                        f"{user[0].email}",
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
                                f"{user[0].profile_text}",
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
                # width=["100%", "49.1%", "32.2%", "32.2%", "24.1%"],
            ),
            as_child=True,
            size="3",
        )


user_card = UserCard.create
