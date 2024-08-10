from typing import Callable
import reflex as rx


def profile_text(
    profile_text: str,
    set_profile_text: Callable
) -> rx.Component:
    '''Render the profile section.'''
    return rx.box(
        rx.desktop_only(
            rx.text_area(
                value=profile_text,
                placeholder="Quelles sont tes passions ?\
                    \nQu'est-ce qui te fait vibrer ?",
                width='100%',
                size='3',
                height='9vh',
                max_length=300,
                on_change=set_profile_text,
            ),
        ),
        rx.tablet_only(
            rx.text_area(
                value=profile_text,
                placeholder="Quelles sont tes passions ?\
                    \nQu'est-ce qui te fait vibrer ?",
                width='100%',
                height='9vh',
                max_length=300,
                on_change=set_profile_text,
            ),
        ),
        rx.mobile_only(
            rx.text_area(
                value=profile_text,
                placeholder="Quelles sont tes passions ?\
                    \nQu'est-ce qui te fait vibrer ?",
                width='100%',
                height='12vh',
                max_length=300,
                on_change=set_profile_text,
            ),
            width='100%',
        ),
        width='100%',
    )
