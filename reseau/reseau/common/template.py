from typing import Callable

import reflex as rx

from ..common.base_state import BaseState
from ..components.feedback_dialog import feedback_dialog
from ..components.sidebar import sidebar
from ..components.site_name import site_name


def template(
    page: Callable[[], rx.Component],
) -> rx.Component:
    return rx.vstack(
        sidebar(),
        rx.cond(
            BaseState.is_authenticated,
            rx.box(
                rx.container(
                    site_name(),
                    page(),
                    size="3",
                ),
                width="100%",
                margin=["12px", "12px", "12px", "48px 0px"],
            ),
            rx.box(
                page(),
            ),
        ),
        rx.cond(
            BaseState.is_authenticated,
            feedback_dialog(
                # user=BaseState.authenticated_user,
            ),
        ),
        width="100%",
    )
