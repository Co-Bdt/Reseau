import reflex as rx

from ...common.base_state import BaseState
from ..private_discussions_popover import private_discussions_popover  # noqa
from ..profile_picture import profile_picture
from ...reseau import GROUPS_ROUTE, HOME_ROUTE, MEMBERS_ROUTE, PROFILE_ROUTE
from ..site_name import site_name


item_style = rx.Style(
    cursor='pointer',
    align='center',
    padding='6px',
    border_radius='0.5em',
    _hover={
        'bg': rx.color('gray', 4),
    },
)

default_tab: str = "home_page"


def navbar(
    current_page: str,
    are_tabs_visible: bool = True,
) -> rx.Component:
    # def sidebar_item(
    #     icon: str, func: Callable, href: str
    # ) -> rx.Component:
    #     '''A sidebar link.'''
    #     return rx.link(
    #         rx.desktop_only(
    #             rx.hstack(
    #                 rx.color_mode_cond(
    #                     light=rx.icon(icon, color='black', size=28),
    #                     dark=rx.icon(icon, color='white', size=28),
    #                 ),
    #                 style=item_style,
    #             ),
    #         ),
    #         rx.mobile_and_tablet(
    #             rx.color_mode_cond(
    #                 light=rx.icon(icon, color='black', size=24),
    #                 dark=rx.icon(icon, color='white', size=24),
    #             ),
    #             padding='6px',
    #             align='center',
    #             style={
    #                 '_hover': {
    #                     'bg': rx.color('gray', 4),
    #                 },
    #                 'border-radius': '0.5em',
    #             },
    #         ),
    #         href=href,
    #         on_click=func,
    #         underline='none',
    #     )

    def sidebar_items() -> rx.Component:
        '''A list of sidebar links.'''

        return rx.hstack(
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

    return rx.vstack(
        rx.hstack(
            site_name(),
            sidebar_items(),
            width='100%',
            justify='start',
            align='center',
            padding_top=['1em', '1em', '1em', '2em'],
            padding_bottom='1em',
        ),
        rx.cond(
            are_tabs_visible,
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(
                        "Communauté",
                        value="home_page",
                        style=rx.Style(
                            cursor='pointer',
                            font_size='1.1em',
                        ),
                        on_click=rx.redirect(HOME_ROUTE),
                    ),
                    rx.tabs.trigger(
                        "Fratries",
                        value="groups_page",
                        style=rx.Style(
                            cursor='pointer',
                            font_size='1.1em',
                        ),
                        on_click=rx.redirect(GROUPS_ROUTE),
                    ),
                    rx.tabs.trigger(
                        "Membres",
                        value="members_page",
                        style=rx.Style(
                            cursor='pointer',
                            font_size='1.1em',
                        ),
                        on_click=rx.redirect(MEMBERS_ROUTE),
                    ),
                    size='2',
                ),
                rx.tabs.content(
                    rx.spacer(),
                    value="home_page",
                ),
                rx.tabs.content(
                    rx.spacer(),
                    value="groups_page",
                ),
                rx.tabs.content(
                    rx.spacer(),
                    value="members_page",
                ),
                default_value=default_tab,
                value=current_page,
                width="100%",
            ),
            rx.tablet_and_desktop(
                rx.vstack(
                    rx.spacer(),
                    rx.box(
                        width='100%',
                        height='1px',
                        style=rx.Style(
                            background_color='#e2e1de'
                        )
                    ),
                    spacing='0',
                    width='100%',
                ),
                width='100%',
            ),
        ),
        spacing='0',
        padding_x=['1em', '1em', '1em', '1em', '0'],
    )
