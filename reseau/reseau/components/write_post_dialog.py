import reflex as rx
from typing import Callable, Tuple

from ..components.autosize import autosize_textarea
from ..models import UserAccount


class WritePostDialog(rx.ComponentState):
    title: str = ""
    content: str = ""

    def clear_fields(self):
        self.title = ""
        self.content = ""

    @classmethod
    def get_component(cls, **props):
        user: Tuple[UserAccount, bool] = props.pop("user")
        publish_post: Callable = props.pop("publish_post")

        return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    "Écris quelque chose",
                    width="100%",
                    size="3",
                    variant="outline",
                    color_scheme="gray",
                    radius="large",
                    style=rx.Style(
                        justify_content="start",
                        background_color="white",
                        font_size=["0.9em", "1em"],
                    ),
                )
            ),
            rx.dialog.content(
                rx.form.root(
                    rx.flex(
                        rx.hstack(
                            rx.cond(
                                user[1],
                                rx.image(
                                    src=rx.get_upload_url(
                                        f"{user[0].id}_profile_picture.png"
                                    ),
                                    width="4vh",
                                    height="4vh",
                                    border="0.5px solid #ccc",
                                    border_radius="50%",
                                ),
                                rx.image(
                                    src=rx.get_upload_url(
                                        "blank_profile_picture.png"
                                    ),
                                    width="4vh",
                                    height="4vh",
                                    border="0.5px solid #ccc",
                                    border_radius="50%",
                                ),
                            ),
                            rx.text(
                                user[0].username,
                                weight="medium",
                            ),
                            align="center",
                            margin_bottom="0.5em",
                        ),
                        rx.text(
                            "Titre",
                            size="2",
                            weight="medium",
                        ),
                        rx.input(
                            id="title",
                            name="title",
                            value=cls.title,
                            on_change=cls.set_title,
                            width="100%",
                            size="3",
                            variant="soft",
                            color_scheme="gray",
                            background_color=rx.color_mode_cond(
                                light="white",
                                dark="#121212",
                            ),
                            color=rx.color_mode_cond(
                                light="black",
                                dark="white",
                            ),
                            style=rx.Style(
                                border="0.5px solid #ccc",
                                font_size=["0.9em", "1em"],
                            ),
                        ),
                        rx.text(
                            "Contenu",
                            size="2",
                            weight="medium",
                            margin_top="1em",
                        ),
                        autosize_textarea(
                            id="content",
                            class_name="autosize-textarea",
                            font_size=["0.9em", "1em"],
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
                        rx.cond(
                            cls.title,
                            rx.dialog.close(
                                rx.form.submit(
                                    rx.button(
                                        "Publier",
                                        type="submit",
                                        on_click=cls.clear_fields,
                                    ),
                                ),
                            ),
                            rx.button(
                                "Publier",
                                disabled=True,
                            ),
                        ),
                        spacing="3",
                        margin_top="16px",
                        justify="end",
                    ),
                    on_submit=publish_post,
                    reset_on_submit=True,
                ),
                padding=["1em 0.5em", "1.5em"],
            ),
        )


write_post_dialog = WritePostDialog.create
