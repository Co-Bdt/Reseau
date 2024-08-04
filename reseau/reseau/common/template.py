from typing import Callable

import reflex as rx

from ..common.base_state import BaseState
from ..components.feedback_dialog import feedback_dialog
from ..components.navbar import navbar


def template(
    page: Callable[[], rx.Component],
) -> rx.Component:
    return rx.vstack(
        rx.cond(
            BaseState.is_authenticated,
            rx.box(
                rx.container(
                    navbar(),
                    page(),
                    size="4",
                    padding_y=["1em", "1em", "1em", "0", "0"],
                    padding_x=["1em", "1em", "1em", "1em", "0"],
                ),
                width="100%",
                margin=["0", "0", "0", "2em 0"],
            ),
            rx.box(
                page(),
            ),
        ),
        rx.cond(
            BaseState.is_authenticated,
            feedback_dialog(),
        ),
        width="100%",
    )
