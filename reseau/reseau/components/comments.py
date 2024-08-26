import reflex as rx
from typing import Tuple

from ..components.profile_picture import profile_picture
from ..models import Comment, UserAccount


def comments(
    post_comments: list[Tuple[Comment, str, UserAccount]],
) -> rx.Component:
    return rx.grid(
        rx.foreach(
            post_comments,
            lambda comment: rx.card(
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
                                style={
                                    "font_weight": "500",
                                    "font_size": ["0.9em", "1em"],
                                },
                                trim="both",
                            ),
                            rx.text(
                                comment[2].last_name,
                                style={
                                    "font_weight": "500",
                                    "font_size": ["0.9em", "1em"],
                                },
                                trim="both",
                            ),
                            rx.text(
                                "•",
                                style={
                                    "font_size": "0.8em",
                                    "color": "gray",
                                },
                                trim="both",
                            ),
                            rx.text(
                                comment[1],
                                style={
                                    "font_size": "0.8em",
                                    "color": "gray",
                                },
                                trim="both",
                            ),
                            spacing="1",
                            align="end",
                        ),
                        rx.text(
                            comment[0].content,
                            style={
                                "font_size": ["0.9em", "1em"],
                            },
                            margin_top="0.5em",
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
