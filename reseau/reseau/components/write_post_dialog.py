import reflex as rx
from typing import Callable

from ..common.base_state import BaseState
from ..components.autosize import autosize_textarea
from ..components.profile_picture import profile_picture
from ..models import UserAccount


dialog_button_style = {
    "width": "100%",
    "size": "3",
    "variant": "outline",
    "color_scheme": "gray",
    "radius": "large",
    "style": rx.Style(
        justify_content="start",
        background_color=rx.color_mode_cond(
            light="white",
            dark="#191918",
        ),
        font_size=["0.9em", "1em"],
        cursor="pointer",
    )
}

title_input_style = {
    "width": "100%",
    "size": "3",
    "variant": "soft",
    "color_scheme": "gray",
    "background_color": rx.color_mode_cond(
        light="white",
        dark="#121212",
    ),
    "color": rx.color_mode_cond(
        light="black",
        dark="white",
    ),
    "style": rx.Style(
        border="0.5px solid #ccc",
        font_size=["0.9em", "1em"],
    ),
}


class WritePostDialogState(BaseState):
    title: str = ""
    content: str = ""

    def clear_fields(self):
        self.title = ""
        self.content = ""


def write_post_dialog(**props):
    user: UserAccount = props.pop("user")
    publish_post: Callable = props.pop("publish_post")

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Écris quelque chose",
                **dialog_button_style,
            )
        ),
        rx.dialog.content(
            rx.form.root(
                rx.flex(
                    rx.hstack(
                        profile_picture(
                            style=rx.Style(
                                width="2.7em",
                                height="2.7em",
                                border="0.5px solid #ccc",
                            ),
                            profile_picture=user.profile_picture,
                        ),
                        rx.text(
                            user.first_name,
                            style={
                                "font_weight": "500",
                                "margin_left": "0.5em",
                            },
                        ),
                        rx.text(
                            user.last_name,
                            style={
                                "font_weight": "500",
                            },
                        ),
                        spacing="1",
                        margin_bottom="0.5em",
                    ),
                    rx.text(
                        "Titre",
                        style={
                            "font_size": "0.9em",
                        },
                        margin_top="1em",
                    ),
                    rx.input(
                        name="title",
                        value=WritePostDialogState.title,
                        on_change=WritePostDialogState.set_title,
                        **title_input_style,
                    ),
                    rx.text(
                        "Contenu",
                        style={
                            "font_size": "0.9em",
                        },
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
                        WritePostDialogState.title,
                        rx.dialog.close(
                            rx.form.submit(
                                rx.button(
                                    "Publier",
                                    type="submit",
                                    on_click=WritePostDialogState.clear_fields,
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
