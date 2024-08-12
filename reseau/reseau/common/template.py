from typing import Callable

import reflex as rx

from ..common.base_state import BaseState
from ..components.feedback_dialog import feedback_dialog
from ..components.navbar import navbar


def template(
    page: Callable[[], rx.Component],
) -> rx.Component:
    return rx.fragment(
        rx.cond(
            BaseState.is_hydrated & BaseState.is_authenticated,
            rx.box(
                rx.box(
                    rx.container(
                        navbar(),
                        size="4",
                    ),
                    rx.separator(),
                    width="100%",
                    margin_bottom=["0", "0", "0", "2em"],
                    padding_top=["0", "0", "0", "2em"],
                    background_color=rx.color_mode_cond(
                        light="white",
                        dark="#212121",
                    ),
                ),
                rx.container(
                    page(),
                    size="4",
                    padding_y=["1em", "1em", "1em", "0", "0"],
                    padding_x=["1em", "1em", "1em", "1em", "0"],
                ),
                feedback_dialog(),
                width="100%",
            ),
            rx.box(
                page(),
            ),
        ),
        width="100%",
    )
