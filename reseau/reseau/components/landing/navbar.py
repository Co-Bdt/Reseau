import reflex as rx

from reseau.components.site_name import site_name
from reseau.reseau import LOGIN_ROUTE, REGISTER_ROUTE


def navbar() -> rx.Component:
    def log_in_button() -> rx.Component:
        return rx.link(
            rx.button(
                rx.tablet_and_desktop('Connexion'),
                rx.mobile_only(
                    rx.icon('log-in'),
                    style=rx.Style(
                        margin_right='0.5em',
                    ),
                ),
                size='3',
                variant='ghost',
                style=rx.Style(
                    color='black',
                    font_family='Inter, sans-serif',
                    font_weight='600',
                    _hover={
                        'bg': rx.color('gray', 4),
                    }
                )
            ),
            href=LOGIN_ROUTE,
        )

    def register_button() -> rx.Component:
        return rx.link(
            rx.button(
                'Rejoindre',
                size='3',
                style=rx.Style(
                    font_family='Inter, sans-serif',
                    font_weight='600',
                )
            ),
            href=REGISTER_ROUTE,
        )

    return rx.vstack(
        rx.hstack(
            site_name(),
            rx.tablet_and_desktop(
                rx.hstack(
                    log_in_button(),
                    register_button(),
                    spacing='6',
                    justify='end',
                    style=rx.Style(
                        width='100%',
                    ),
                ),
                width='100%',
            ),
            rx.mobile_only(
                rx.hstack(
                    log_in_button(),
                    justify='end',
                    style=rx.Style(
                        width='100%',
                    ),
                ),
                width='100%',
            ),
            align='center',
            justify='start',
            style=rx.Style(
                width='100%',
                padding_x=['1em', '1em', '1em', '1em', '0'],
                padding_top='1em',
            ),
        ),
        rx.box(
            style=rx.Style(
                width='100%',
                height='1px',
                background_color='rgba(229,231,235,0.2)',
            ),
        ),
        spacing='4',
    ),
