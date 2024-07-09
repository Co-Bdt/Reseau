import reflex as rx

from ..reseau import REGISTER_ROUTE


def landing() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Rɘseau",
            size="9",
            style={
                "font-family": "Droid Sans Mono",
                "letter-spacing": "1px"
            }
        ),
        rx.desktop_only(
            rx.text(
                "La première plateforme pour connaître ",
                "des gars en développement personnel",
                size="5",
            ),
        ),
        rx.mobile_and_tablet(
            rx.text(
                "La première plateforme pour rencontrer ",
                "des gars en développement personnel",
                size="4",
            ),
        ),
        rx.link(
            rx.button("Rejoindre", size="3"),
            href=REGISTER_ROUTE,
            is_external=False
        ),
        spacing="5",
        justify="center",
    )
