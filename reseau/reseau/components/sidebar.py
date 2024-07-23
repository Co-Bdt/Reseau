import reflex as rx
from typing import Callable

from ..reseau import MEMBERS_ROUTE, PROFILE_ROUTE, HOME_ROUTE
from ..common.base_state import BaseState


class Sidebar(rx.ComponentState):
    is_open: bool = False

    def toggle(self):
        self.is_open = not self.is_open

    @classmethod
    def get_component(cls, **props):
        def sidebar_item(
            text: str, icon: str, func: Callable, href: str
        ) -> rx.Component:
            """A sidebar link."""
            return rx.link(
                rx.hstack(
                    rx.color_mode_cond(
                        light=rx.icon(icon, color="black"),
                        dark=rx.icon(icon, color="white"),
                    ),
                    width="100%",
                    padding_x="6px",
                    padding_y="6px",
                    align="center",
                    style={
                        "_hover": {
                            "bg": rx.color("gray", 4),
                        },
                        "border-radius": "0.5em",
                    },
                ),
                href=href,
                on_click=func,
                underline="none",
                width="100%",
            )

        def sidebar_items() -> rx.Component:
            """A list of sidebar links."""
            return rx.vstack(
                sidebar_item("Home", "school", None, HOME_ROUTE),
                rx.cond(
                    BaseState.is_authenticated,
                    sidebar_item(
                        "Membres",
                        "user-search",
                        None,
                        MEMBERS_ROUTE),
                ),
                rx.cond(
                    BaseState.is_authenticated,
                    sidebar_item(
                        "Profil",
                        "user",
                        None,
                        PROFILE_ROUTE,),
                ),
                rx.cond(
                    BaseState.is_authenticated,
                    sidebar_item(
                        "Compte",
                        "log-out",
                        BaseState.do_logout,
                        HOME_ROUTE),
                ),
                spacing="2",
                width="100%",
            )

        return rx.box(
            rx.desktop_only(
                rx.vstack(
                    sidebar_items(),
                    position="fixed",
                    left="50px",
                    top="50px",
                    padding_x="1em",
                    padding_y="1em",
                    align="start",
                ),
            ),
            rx.mobile_and_tablet(
                # rx.icon_button(
                #     rx.icon(
                #         "plus",
                #     ),
                #     position="absolute",
                #     right="15px",
                #     top="15px",
                #     variant="solid",
                #     # color_scheme="blue",
                #     size="3",
                #     radius="full",
                #     on_click=cls.toggle(),
                # ),
                rx.vstack(
                    sidebar_items(),
                    position="fixed",
                    right="0px",
                    top="0px",
                    padding_x="1em",
                    padding_y="1em",
                    align="start",
                ),
                # rx.cond(
                #     cls.is_open,
                #     sidebar_items(),
                # ),
            ),
            **props,
        )


sidebar = Sidebar.create
