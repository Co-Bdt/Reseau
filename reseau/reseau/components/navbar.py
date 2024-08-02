import reflex as rx
from typing import Callable

from ..reseau import MEMBERS_ROUTE, PROFILE_ROUTE
from ..common.base_state import BaseState
from .site_name import site_name


class Navbar(rx.ComponentState):
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
                        light=rx.icon(icon, color="black", size=28),
                        dark=rx.icon(icon, color="white", size=28),
                    ),
                    padding="6px",
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
            )

        def sidebar_items() -> rx.Component:
            """A list of sidebar links."""
            return rx.hstack(
                rx.cond(
                    BaseState.is_authenticated,
                    sidebar_item(
                        "Membres",
                        "user-search",
                        None,
                        MEMBERS_ROUTE),
                ),
                rx.link(
                    rx.image(
                        src=rx.get_upload_url(
                            f"{BaseState.authenticated_user.id}_profile_picture.png"
                        ),
                        border="0.5px solid #ccc",
                        width="3vh",
                        height="3vh",
                        border_radius="50%",
                    ),
                    href=PROFILE_ROUTE,
                    padding="6px",
                ),
                spacing="4",
                width="100%",
                justify="end",
            )

        return rx.box(
            rx.desktop_only(
                rx.hstack(
                    site_name(),
                    sidebar_items(),
                    width="100%",
                    justify="start",
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
        )


navbar = Navbar.create
