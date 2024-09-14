from typing import Callable
import reflex as rx


common_style = rx.Style(
    width='100%',
    height='9vh',
    border_radius='10px',
)


def profile_text(
    profile_text: str,
    set_profile_text: Callable
) -> rx.Component:
    '''Render the profile section.'''
    return rx.box(
        rx.desktop_only(
            rx.text_area(
                value=profile_text,
                placeholder="Qui es-tu ?\
                    \nQu'est-ce qui te caractérise ?",
                size='3',
                max_length=300,
                on_change=set_profile_text,
                style=common_style,
            ),
        ),
        rx.tablet_only(
            rx.text_area(
                value=profile_text,
                placeholder="Qui es-tu ?\
                    \nQu'est-ce qui te caractérise ?",
                max_length=300,
                on_change=set_profile_text,
                style=common_style,
            ),
        ),
        rx.mobile_only(
            rx.text_area(
                value=profile_text,
                placeholder="Qui es-tu ?\
                    \nQu'est-ce qui te caractérise ?",
                max_length=300,
                on_change=set_profile_text,
                style=rx.Style(
                    width='100%',
                    height='12vh',
                    border_radius='10px',
                ),
            ),
            width='100%',
        ),
        width='100%',
    )
