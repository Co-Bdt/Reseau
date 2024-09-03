import reflex as rx
from typing import Callable

# from reseau.pages.home import HomeState

# from ..pages.members import MembersState, members_page

from ..common.base_state import BaseState
from ..components.private_discussions_popover import private_discussions_popover  # noqa
from ..components.profile_picture import profile_picture
from ..reseau import MEMBERS_ROUTE, PROFILE_ROUTE
from .site_name import site_name


item_style = rx.Style(
    cursor='pointer',
    align='center',
    padding='6px',
    border_radius='0.5em',
    _hover={
        'bg': rx.color('gray', 4),
    },
)


class NavbarState(rx.State):
    default_tab: str = "community"

    # def on_tab_change(self, value):
    #     if value == "community":
    #         return HomeState.init()
    #     elif value == "members":
    #         return MembersState.init()


def navbar() -> rx.Component:
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
                    style=item_style,
                ),
            ),
            rx.mobile_and_tablet(
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
                    MEMBERS_ROUTE
                ),
            ),
            rx.cond(
                BaseState.is_authenticated,
                private_discussions_popover()
            ),
            rx.hstack(
                rx.link(
                    profile_picture(
                        style=rx.Style(
                            width=['1.8em', '1.8em', '1.8em', '2em'],
                            height=['1.8em', '1.8em', '1.8em', '2em'],
                        ),
                        profile_picture=(
                            BaseState.authenticated_user.profile_picture
                        ),
                    ),
                    href=PROFILE_ROUTE,
                ),
                style=item_style,
                padding='4px',
            ),
            spacing='5',
            width='100%',
            justify='end',
            align='center',
        )

    return rx.box(
        rx.tablet_and_desktop(
            rx.vstack(
                rx.hstack(
                    site_name(),
                    sidebar_items(),
                    width='100%',
                    padding_top='1em',
                    # padding_bottom=['1em', '1em', '1em', '2em'],
                    justify='start',
                    align='center',
                ),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(
                            "Communauté",
                            # margin_left='5em',
                        ),
                        rx.tabs.trigger(
                            rx.link("Membres", href=MEMBERS_ROUTE),
                            # value="members"
                        ),
                    ),
                    # rx.tabs.content(
                    #     rx.text("item on tab 1"),
                    #     value="community",
                    # ),
                    # rx.tabs.content(
                    #     members_page(),
                    #     value="members",
                    # ),
                    default_value=NavbarState.default_tab,
                    # on_change=lambda value: NavbarState.on_tab_change(value),
                    width="100%",
                ),
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
