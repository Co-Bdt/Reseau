from typing import Callable

import reflex as rx

from ..common.base_state import BaseState
from ..common.navbar import navbar
from ..components.feedback_dialog import feedback_dialog


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
                            are_tabs_visible=page.__name__ != 'profile_page',
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
                                        "Plusieurs canaux de discussions sont "
                                        "maintenant disponibles ! N'hésite "
                                        "pas à faire un retour sur la "
                                        "prochaine fonctionnalité que tu "
                                        "aimerais avoir",
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
                    margin_bottom=['0', '0', '0', '1.75em'],
                    padding_top=['0', '0', '0', '1.5em'],
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
        width='100%',
    )
