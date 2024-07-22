from typing import Callable

import reflex as rx


def write_post_dialog(
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
                style=rx.Style(justify_content="start")
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Nouveau post [user?]"),
            rx.form.root(
                rx.flex(
                    rx.input(
                        name="title",
                        placeholder="Titre",
                        width="100%",
                        size="2",
                        variant="soft",
                        style=rx.Style(background_color="white"),
                    ),
                    rx.input(
                        name="content",
                        placeholder="Écris quelque chose...",
                        width="100%",
                        size="2",
                        variant="soft",
                        autofocus=True,
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
