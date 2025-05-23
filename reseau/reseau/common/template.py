from typing import Callable

import reflex as rx

from ..common.base_state import BaseState
from ..components.common.navbar import navbar
from ..components.feedback_dialog import feedback_dialog


banner_text = (
    "La prochaine grosse nouveauté sera un système de groupes basés sur ",
    "un intérêt ou un business commun : les Fratries. ",
    "Dis nous ce que tu en penses !",
)


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
                            are_tabs_visible=(
                                page.__name__ != 'profile_page' and
                                page.__name__ != 'group_page'
                            ),
                        ),
                        size='4',
                        padding='0',
                    ),
                    rx.box(
                        margin_top='-1px',
                        width='calc((100vw - var(--container-4)) / 2)',
                        height='1px',
                        style=rx.Style(
                            background_color='#e2e1de'
                        )
                    ),
                    rx.box(
                        margin_top='-1px',
                        position='absolute',
                        right='0',
                        width='calc((100vw - var(--container-4)) / 2)',
                        height='1px',
                        style=rx.Style(
                            background_color='#e2e1de'
                        )
                    ),
                    rx.cond(
                        page.__name__ == 'home_page',
                        rx.desktop_only(
                            rx.box(
                                rx.container(
                                    rx.text(
                                        banner_text,
                                        class_name='mobile-text',
                                        style=rx.Style(
                                            font_color='gray',
                                            font_family='Satoshi Variable, '
                                                        'sans-serif',
                                        ),
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
                    background_color=rx.color_mode_cond(
                        light='white',
                        dark='#212121',
                    ),
                ),
                rx.container(
                    page(),
                    size='4',
                    padding_x=['1em', '1em', '1em', '1em', '0'],
                    padding_top='1em',
                    padding_bottom=['1em', '1em', '1em', '4em'],
                    height='100%',
                ),
                feedback_dialog(
                    BaseState.authenticated_user,
                ),
                class_name='root-box',
                min_height='100dvh',
                width='100%',
            ),
            rx.box(
                page(),
            ),
        ),
        height='100%',
        width='100%',
    )
