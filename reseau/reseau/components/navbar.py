import reflex as rx
from typing import Callable


from ..common.base_state import BaseState
from ..components.private_discussion import private_discussion
from ..components.profile_picture import profile_picture
from ..reseau import MEMBERS_ROUTE, PROFILE_ROUTE
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
        from ..pages.private_discussions import PrivateDiscussionsState

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
                # sidebar_item(
                #     'message-square',
                #     None,
                #     PRIVATE_DISCUSSIONS_ROUTE
                # ),
                rx.button(
                    "Discussions",
                    # rx.menu.root(
                    #     rx.menu.trigger(
                    #         rx.icon(
                    #             'message-square',
                    #             size=28,
                    #         ),
                    #     ),
                    #     rx.menu.content(
                    #         rx.text(
                    #             "Discussions",
                    #             font_weight='500',
                    #         ),
                    #         rx.foreach(
                    #             PrivateDiscussionsState.private_discussions,
                    #             lambda discussion: rx.dialog.root(
                    #                 rx.dialog.trigger(
                    #                     rx.card(
                    #                         rx.text(
                    #                             f"{discussion.first_name} "
                    #                             f"{discussion.last_name}"
                    #                         ),
                    #                     ),
                    #                     on_click=PrivateDiscussionsState.load_private_messages(  # noqa: E501
                    #                         discussion.id
                    #                     ),
                    #                 ),
                    #                 rx.dialog.content(
                    #                     rx.dialog.title(
                    #                         rx.text(
                    #                             f"{discussion.first_name} "
                    #                             f"{discussion.last_name}"
                    #                         ),
                    #                     ),
                    #                     private_discussion(
                    #                         authenticated_user=PrivateDiscussionsState.authenticated_user,  # noqa: E501
                    #                         other_user=discussion,
                    #                         messages=PrivateDiscussionsState.discussion_messages,  # noqa: E501
                    #                         send_message=PrivateDiscussionsState.send_message
                    #                     )
                    #                 )
                    #             ),
                    #         ),
                    #         padding='0.8em',
                    #     ),
                    # ),
                    on_click=rx.call_script(
                        """
                        console.log("navbar on_click")
                        """
                    ),
                ),
            ),
            rx.link(
                profile_picture(
                    style=rx.Style(
                        width=['1.8em', '1.8em', '1.8em', '2em'],
                        height=['1.8em', '1.8em', '1.8em', '2em'],
                    ),
                    profile_picture=(
                        NavbarState.authenticated_user.profile_picture
                    ),
                ),
                href=PROFILE_ROUTE,
                padding='6px',
            ),
            spacing='5',
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
