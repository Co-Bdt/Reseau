from typing import Callable

import reflex as rx

from ..models.comment import Comment
from ..models.post import Post


def post_dialog(
    post: Post,
    post_comments: list[Comment],
    load_post_comments: Callable,
    publish_comment: Callable,
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.card(
                rx.text(
                    f"{post.title} - \
                        {post.published_at}"
                ),
                rx.text(f"{post.content}"),
                width="100%",
            ),
            on_click=load_post_comments(post.id)
        ),
        rx.dialog.content(
            # rx.dialog.title(post.title),
            rx.flex(
                rx.text(f"{post.published_at}"),
                rx.text(f"{post.content}"),

                # comments of the post
                rx.text("Commentaires", size="4", font_weight="bold"),
                rx.grid(
                    rx.foreach(
                        post_comments,
                        lambda comment: rx.card(
                            rx.text(
                                comment.published_at,
                            ),
                            rx.text(comment.content),
                            width="100%",
                        ),
                    ),
                    columns="1",
                    width="100%",
                ),

                # form to comment the post
                rx.form.root(
                    rx.input(
                        name="post_id",
                        value=post.id,
                        style=rx.Style(display="none"),
                    ),
                    rx.input(
                        name="content",
                        placeholder="Commente...",
                        width="100%",
                        size="2",
                        autofocus=True,
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
                                    "Commenter",
                                    type="submit",
                                ),
                            ),
                        ),
                        spacing="3",
                        margin_top="16px",
                        justify="end",
                    ),
                    on_submit=publish_comment
                ),
                direction="column",
                spacing="2",
            ),
        ),
    ),
