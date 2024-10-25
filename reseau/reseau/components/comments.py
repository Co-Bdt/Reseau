import reflex as rx
from typing import Tuple

from ..components.profile_picture import profile_picture
from ..models import Comment, UserAccount


name_style = rx.Style(
    font_family='Satoshi, sans-serif',
    font_weight='600',
    font_size=["0.9em", "1em"],
)

date_style = rx.Style(
    color='gray',
    font_family='Satoshi, sans-serif',
    font_size='0.8em',
)


def comments(
    post_comments: list[Tuple[Comment, str, UserAccount]],
) -> rx.Component:
    return rx.grid(
        rx.foreach(
            post_comments,
            lambda comment: rx.box(
                rx.hstack(
                    profile_picture(
                        style=rx.Style(
                            width="2.5em",
                            height="2.5em",
                        ),
                        profile_picture=comment[2].profile_picture,
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text(
                                comment[2].first_name,
                                trim="both",
                                style=name_style
                            ),
                            rx.text(
                                comment[2].last_name,
                                trim="both",
                                style=name_style
                            ),
                            rx.text(
                                "•",
                                trim="both",
                                style=date_style
                            ),
                            rx.text(
                                comment[1],
                                trim="both",
                                style=date_style
                            ),
                            spacing="1",
                            align="end",
                        ),
                        rx.text(
                            comment[0].content,
                            style=rx.Style(
                                font_family='Satoshi, sans-serif',
                                font_size=["0.9em", "1em"],
                            ),
                            margin_top="0.5em",
                        ),
                        spacing="0",
                    ),
                ),
                width="100%",
                background_color='#f8f7f5',
                padding=["1em", "1.5em"],
                border_radius='0',
            ),
        ),
        columns="1",
        width="100%",
        spacing="3",
        border_radius="0",
        border='none',
    ),
