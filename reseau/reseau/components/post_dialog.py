from typing import Callable, Tuple
import reflex as rx

from ..components.comments import comments
from ..components.write_comment_form import write_comment_form
from ..models import Comment, Post, UserAccount


class PostDialog(rx.ComponentState):

    @classmethod
    def get_component(cls, **props):
        post: Post = props.pop("post", None)
        post_datetime: str = props.pop("post_datetime", "")
        author: UserAccount = props.pop("post_author", None)
        post_comments: list[Tuple[Comment, str, UserAccount]] = props.pop(
            "post_comments", []
        )
        load_post_details: Callable = props.pop("load_post_details")
        publish_comment: Callable = props.pop("publish_comment")

        return rx.dialog.root(
            rx.dialog.trigger(
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.image(
                                src=rx.get_upload_url(
                                    f"{author.id}_profile_picture"
                                ),
                                border="0.5px solid #ccc",
                                width="4vh",
                                height="4vh",
                                border_radius="50%",
                            ),
                            rx.vstack(
                                rx.text(
                                    author.username,
                                    weight="medium",
                                ),
                                rx.text(
                                    post_datetime,
                                    size="1",
                                    color_scheme="gray",
                                ),
                                spacing="0",
                            ),
                        ),
                        rx.text(
                            post.title,
                            size="4",
                            weight="bold",
                        ),
                        rx.text(
                            post.content,
                        ),
                        width="100%",
                    ),
                    padding="1.2em",
                    cursor="pointer",
                ),
                on_click=load_post_details(post.id)
            ),
            rx.dialog.content(
                rx.flex(
                    rx.hstack(
                        rx.image(
                            src=rx.get_upload_url(
                                f"{author.id}_profile_picture"
                            ),
                            border="0.5px solid #ccc",
                            width="4vh",
                            height="4vh",
                            border_radius="50%",
                        ),
                        rx.vstack(
                            rx.text(
                                author.username,
                                weight="medium",
                            ),
                            rx.text(
                                post_datetime,
                                size="1",
                                color_scheme="gray",
                            ),
                            spacing="0",
                        ),
                    ),
                    rx.text(post.title, size="5", weight="bold"),
                    rx.text(post.content),

                    rx.separator(),
                    # comments of the post
                    comments(
                        post_comments,
                    ),
                    # form to comment the post
                    write_comment_form(
                        post=post,
                        publish_comment=publish_comment,
                    ),
                    direction="column",
                    spacing="4",
                ),
            ),
        )


post_dialog = PostDialog.create
