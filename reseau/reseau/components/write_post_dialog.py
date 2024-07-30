import reflex as rx
from typing import Callable

from ..models import UserAccount


def write_post_dialog(
    user: UserAccount,
    publish_post: Callable,
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Écris quelque chose",
                width="100%",
                size="3",
                variant="outline",
                color_scheme="gray",
                radius="large",
                style=rx.Style(justify_content="start"),
            )
        ),
        rx.dialog.content(
            rx.form.root(
                rx.flex(
                    rx.hstack(
                        rx.image(
                            src=rx.get_upload_url(
                                f"{user.id}_profile_picture"
                            ),
                            width="4vh",
                            height="4vh",
                            border="0.5px solid #ccc",
                            border_radius="50%",
                        ),
                        rx.text(
                            user.username,
                            weight="medium",
                        ),
                        align="center",
                        margin_bottom="0.5em",
                    ),
                    rx.input(
                        name="title",
                        placeholder="Titre",
                        width="100%",
                        size="3",
                        variant="soft",
                        style=rx.Style(
                            background_color="white",
                            color="black"
                        ),
                    ),
                    rx.text_area(
                        name="content",
                        placeholder="Écris quelque chose...",
                        width="100%",
                        size="2",
                        variant="soft",
                        autofocus=True,
                        rows="2",
                        style=rx.Style(background_color="white"),
                    ),
                    direction="column",
                    spacing="2",
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Annuler",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    rx.dialog.close(
                        rx.form.submit(
                            rx.button(
                                "Publier",
                                type="submit",
                            ),
                        ),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                on_submit=publish_post,
            ),
        ),
    ),
