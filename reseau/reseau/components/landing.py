import reflex as rx

from ..reseau import REGISTER_ROUTE


def landing() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Reseau",
            size="9",
            style={
                "letter-spacing": "1px"
            }
        ),
        rx.desktop_only(
            rx.text(
                "La première plateforme pour connecter avec ",
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
