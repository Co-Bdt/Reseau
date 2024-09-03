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
                        navbar(
                            current_page=page.__name__,
                        ),
                        size='4',
                        padding='0',
                    ),
                    rx.separator(
                        margin_top='-1px',
                    ),
                    rx.cond(
                        page.__name__ == 'home_page',
                        rx.desktop_only(
                            rx.box(
                                rx.container(
                                    rx.text(
                                        "Les messages privés sont maintenant "
                                        "disponibles ! N'hésite pas à faire "
                                        "un retour sur la prochaine "
                                        "fonctionnalité que tu aimerais "
                                        "avoir",
                                        class_name='mobile-text',
                                        font_color='gray',
                                    ),
                                    size='4',
                                    max_height='2em',
                                    padding_y='0.25em',
                                ),
                                width='100%',
                                background_color='var(--blue-3)',
                            ),
                        ),
                    ),
                    width='100%',
                    margin_bottom=['0', '0', '0', '2em'],
                    padding_top=['0', '0', '0', '2em'],
                    background_color=rx.color_mode_cond(
                        light='white',
                        dark='#212121',
                    ),
                ),
                rx.container(
                    page(),
                    size='4',
                    padding_x=['1em', '1em', '1em', '1em', '0'],
                    padding_top=['1em', '1em', '1em', '0', '0'],
                    padding_bottom=['1em', '1em', '1em', '4em'],
                ),
                feedback_dialog(),
                class_name='root-box',
                min_height='100dvh',
                width='100%',
            ),
            rx.box(
                page(),
            ),
        ),
        width='100%',
    )
