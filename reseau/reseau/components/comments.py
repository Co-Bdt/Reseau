import reflex as rx
from typing import Tuple

from ..models import Comment, UserAccount


def comments(
    post_comments: list[Tuple[Comment, str, UserAccount, bool]],
) -> rx.Component:
    return rx.grid(
        rx.foreach(
            post_comments,
            lambda comment: rx.card(
                rx.hstack(
                    rx.cond(
                        comment[3],
                        rx.image(
                            src=rx.get_upload_url(
                                f"{comment[0].author_id}_profile_picture.png"
                            ),
                            border="0.5px solid #ccc",
                            width="4vh",
                            height="4vh",
                            border_radius="50%",
                        ),
                        rx.image(
                            src=rx.get_upload_url("blank_profile_picture.png"),
                            border="0.5px solid #ccc",
                            width="4vh",
                            height="4vh",
                            border_radius="50%",
                        ),
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text(
                                comment[2].username,
                                weight="medium",
                                trim="both",
                                font_size=["0.9em", "1em"],
                            ),
                            rx.text(
                                "•",
                                size="1",
                                color_scheme="gray",
                                trim="both",
                            ),
                            rx.text(
                                comment[1],
                                size="1",
                                color_scheme="gray",
                                trim="both",
                            ),
                            spacing="1",
                            align="end",
                        ),
                        rx.text(
                            comment[0].content,
                            margin_top="0.5em",
                            font_size=["0.9em", "1em"],
                        ),
                        spacing="0",
                    ),
                ),
                width="100%",
                background_color=rx.color_mode_cond(
                    light="#e9e9e9",
                    dark="#191918",
                ),
                padding=["1em 0.5em", "1em"],
            ),
        ),
        columns="1",
        width="100%",
        spacing="3",
    ),
