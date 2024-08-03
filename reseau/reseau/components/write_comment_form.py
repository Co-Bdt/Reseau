from typing import Callable
import reflex as rx

from ..models import Post


class WriteCommentForm(rx.ComponentState):
    comment_value: str = ""

    @classmethod
    def get_component(cls, **props):
        post: Post = props.pop("post")
        publish_comment: Callable = props.pop("publish_comment")
        return rx.form.root(
            rx.input(
                name="post_id",
                value=post.id,
                style=rx.Style(display="none"),
            ),
            rx.input(
                name="content",
                placeholder="Commente...",
                value=cls.comment_value,
                on_change=cls.set_comment_value,
                width="100%",
                size="3",
                radius="large",
                font_size=["0.9em", "1em"],
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
                    cls.comment_value,
                    rx.form.submit(
                        rx.button(
                            "Commenter",
                            type="submit",
                            on_click=cls.set_comment_value(""),
                        ),
                    ),
                    rx.button(
                        "Commenter",
                        disabled=True,
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            on_submit=publish_comment
        )


write_comment_form = WriteCommentForm.create
