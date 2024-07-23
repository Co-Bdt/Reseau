from typing import Callable
import reflex as rx


def profile(
    profile_text: str,
    set_profile_text: Callable
) -> rx.Component:
    """Render the profile section."""
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.text_area(
                    value=profile_text,
                    placeholder="Quelles sont tes passions ?\
                        \nQu'est-ce qui te fait vibrer ?",
                    width="100%",
                    size="3",
                    height="9vh",
                    max_length=300,
                    rows="2",
                    on_change=set_profile_text,
                ),
            ),
            width="100%",
        ),
        rx.mobile_and_tablet(
            rx.vstack(
                rx.text_area(
                    value=profile_text,
                    placeholder="Quelles sont tes passions ?\
                        \nQu'est-ce qui te fait vibrer ?",
                    width="100%",
                    size="3",
                    height="11vh",
                    max_length=300,
                    rows="4",
                    on_change=set_profile_text,
                ),
                width="100%",
            ),
            width="100%",
        ),
        width="100%",
    )
