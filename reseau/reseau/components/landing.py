import reflex as rx

from ..reseau import REGISTER_ROUTE


def landing() -> rx.Component:
    return rx.vstack(
        rx.desktop_only(
            rx.heading(
                "Reseau",
                trim='start',
                style={
                    'font_size': '2.25em',
                    'letter-spacing': '1px',
                    'margin': '0',
                }
            ),
        ),
        rx.mobile_and_tablet(
            rx.heading(
                "Reseau",
                trim='start',
                style={
                    'font_size': '2em',
                    'letter-spacing': '1px',
                    'margin': '0',
                }
            ),
        ),
        rx.desktop_only(
            rx.text(
                "La première plateforme pour connecter avec ",
                "des gars en développement personnel",
                style={
                    'font_size': '1.1em',
                },
            ),
        ),
        rx.mobile_and_tablet(
            rx.text(
                "La première plateforme pour connecter avec ",
                "des gars en développement personnel",
                class_name='desktop-text',
            ),
        ),
        rx.link(
            rx.button("Rejoindre", size='3'),
            href=REGISTER_ROUTE,
            is_external=False
        ),
        spacing='5',
        justify='center',
    )
