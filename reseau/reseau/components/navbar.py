import reflex as rx
from typing import Callable

from ..reseau import MEMBERS_ROUTE, PROFILE_ROUTE
from ..common.base_state import BaseState
from .site_name import site_name


class Navbar(rx.ComponentState):

    @classmethod
    def get_component(cls, **props):
        def sidebar_item(
            icon: str, func: Callable, href: str
        ) -> rx.Component:
            """A sidebar link."""
            return rx.link(
                rx.tablet_and_desktop(
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
                ),
                rx.mobile_only(
                    rx.hstack(
                        rx.color_mode_cond(
                            light=rx.icon(icon, color="black", size=24),
                            dark=rx.icon(icon, color="white", size=24),
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
                        "user-search",
                        None,
                        MEMBERS_ROUTE),
                ),
                rx.link(
                    rx.image(
                        src=rx.get_upload_url(
                            f"{BaseState.authenticated_user.id}"
                            "_profile_picture.png"
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
                align="center",
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
                rx.hstack(
                    site_name(),
                    sidebar_items(),
                    padding_y="1em",
                    padding_x="0.8em",
                    justify="start",
                    align="center",
                ),
            ),
        )


navbar = Navbar.create
