import reflex as rx

from ..models.user_account import UserAccount
from ..models.city import City


def user_card(
    user: UserAccount,
    city: City,
    is_profile_empty: bool
) -> rx.Component:
    return rx.card(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        f"{user.username}",
                        size="2",
                        weight="medium",
                    ),
                    rx.spacer(),
                    rx.text(
                        f"{city.name} ({city.postal_code})",
                        size="2",
                        color_scheme="gray",
                        style={"text-align": "end"}
                    ),
                    width="100%",
                    align="center",
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
                    margin="1em 0 0 0"
                ),
            ),
            width=["100%", "100%", "100%", "24.45%"],
        ),
        as_child=True,
        size="3",
    )
