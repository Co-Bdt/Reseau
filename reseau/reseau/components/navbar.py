import reflex as rx
from typing import Callable


from ..common.base_state import BaseState
from ..components.profile_picture import profile_picture
from ..reseau import MEMBERS_ROUTE, PRIVATE_DISCUSSIONS_ROUTE, PROFILE_ROUTE
from .site_name import site_name


class NavbarState(BaseState):
    ...


def navbar():
    def sidebar_item(
        icon: str, func: Callable, href: str
    ) -> rx.Component:
        '''A sidebar link.'''
        return rx.link(
            rx.desktop_only(
                rx.hstack(
                    rx.color_mode_cond(
                        light=rx.icon(icon, color='black', size=28),
                        dark=rx.icon(icon, color='white', size=28),
                    ),
                    padding='6px',
                    align='center',
                    style={
                        '_hover': {
                            'bg': rx.color('gray', 4),
                        },
                        'border-radius': '0.5em',
                    },
                ),
            ),
            rx.mobile_and_tablet(
                rx.hstack(
                    rx.color_mode_cond(
                        light=rx.icon(icon, color='black', size=24),
                        dark=rx.icon(icon, color='white', size=24),
                    ),
                    padding='6px',
                    align='center',
                    style={
                        '_hover': {
                            'bg': rx.color('gray', 4),
                        },
                        'border-radius': '0.5em',
                    },
                ),
            ),
            href=href,
            on_click=func,
            underline='none',
        )

    def sidebar_items() -> rx.Component:
        '''A list of sidebar links.'''
        return rx.hstack(
            rx.cond(
                BaseState.is_authenticated,
                sidebar_item(
                    'user-search',
                    None,
                    MEMBERS_ROUTE),
            ),
            rx.cond(
                BaseState.is_authenticated,
                sidebar_item(
                    'mail',
                    None,
                    PRIVATE_DISCUSSIONS_ROUTE),
            ),
            rx.link(
                profile_picture(
                    style=rx.Style(
                        width='2.2em',
                        height='2.2em',
                    ),
                    profile_picture=(
                        NavbarState.authenticated_user.profile_picture
                    ),
                ),
                href=PROFILE_ROUTE,
                padding='6px',
            ),
            spacing='4',
            width='100%',
            justify='end',
            align='center',
        )

    return rx.box(
        rx.tablet_and_desktop(
            rx.hstack(
                site_name(),
                sidebar_items(),
                width='100%',
                padding_top='1em',
                padding_bottom=['1em', '1em', '1em', '2em'],
                justify='start',
                align='center',
            ),
        ),
        rx.mobile_only(
            rx.hstack(
                site_name(),
                sidebar_items(),
                padding_y='1em',
                justify='start',
                align='center',
            ),
        ),
    )
