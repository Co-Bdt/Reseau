from typing import Callable
import reflex as rx

from ..models import Post


class WriteCommentForm(rx.ComponentState):
    is_comment_empty: bool = True

    def handle_comment_change(self, comment_value):
        if comment_value:
            self.is_comment_empty = False
        else:
            self.is_comment_empty = True

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
                on_change=cls.handle_comment_change,
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
                    cls.is_comment_empty,
                    rx.button(
                        "Commenter",
                        disabled=True,
                    ),
                    rx.form.submit(
                        rx.button(
                            "Commenter",
                            type="submit",
                        ),
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            on_submit=publish_comment,
            reset_on_submit=True,
        )


write_comment_form = WriteCommentForm.create
