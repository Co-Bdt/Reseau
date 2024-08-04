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
        post_author: UserAccount = props.pop("post_author", None)
        post_profile_picture_exist: bool = (
            props.pop("post_profile_picture_exist", False)
        )

        post_comments: list[Tuple[Comment, str, UserAccount, bool]] = (
            props.pop("post_comments", [])
        )
        load_post_details: Callable = props.pop("load_post_details")
        publish_comment: Callable = props.pop("publish_comment")

        return rx.dialog.root(
            rx.dialog.trigger(
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.cond(
                                post_profile_picture_exist,
                                rx.image(
                                    src=rx.get_upload_url(
                                        f"{post_author.id}_profile_picture.png"
                                    ),
                                    border="0.5px solid #ccc",
                                    width="4vh",
                                    height="4vh",
                                    border_radius="50%",
                                ),
                                rx.image(
                                    src=rx.get_upload_url(
                                        "blank_profile_picture.png"
                                    ),
                                    border="0.5px solid #ccc",
                                    width="4vh",
                                    height="4vh",
                                    border_radius="50%",
                                ),
                            ),
                            rx.vstack(
                                rx.tablet_and_desktop(
                                    rx.text(
                                        post_author.username,
                                        weight="medium",
                                    ),
                                ),
                                rx.mobile_only(
                                    rx.text(
                                        post_author.username,
                                        weight="medium",
                                        size="2",
                                    ),
                                ),
                                rx.text(
                                    post_datetime,
                                    size="1",
                                    color_scheme="gray",
                                ),
                                spacing="0",
                            ),
                        ),
                        rx.tablet_and_desktop(
                            rx.text(
                                post.title,
                                size="4",
                                weight="bold",
                                margin_bottom="0.5em",
                            ),
                            rx.text(
                                post.content,
                            ),
                        ),
                        rx.mobile_only(
                            rx.text(
                                post.title,
                                size="2",
                                weight="bold",
                                margin_bottom="0.3em",
                            ),
                            rx.text(
                                post.content,
                                font_size=["0.8em", "1em"],
                            ),
                        ),
                        width="100%",
                    ),
                    padding=["1em", "1.2em"],
                    cursor="pointer",
                ),
                on_click=load_post_details(post.id)
            ),
            rx.dialog.content(
                rx.flex(
                    rx.hstack(
                        rx.cond(
                            post_profile_picture_exist,
                            rx.image(
                                src=rx.get_upload_url(
                                    f"{post_author.id}_profile_picture.png"
                                ),
                                border="0.5px solid #ccc",
                                width="4vh",
                                height="4vh",
                                border_radius="50%",
                            ),
                            rx.image(
                                src=rx.get_upload_url(
                                    "blank_profile_picture.png"
                                ),
                                border="0.5px solid #ccc",
                                width="4vh",
                                height="4vh",
                                border_radius="50%",
                            ),
                        ),
                        rx.vstack(
                            rx.tablet_and_desktop(
                                    rx.text(
                                        post_author.username,
                                        weight="medium",
                                    ),
                            ),
                            rx.mobile_only(
                                rx.text(
                                    post_author.username,
                                    weight="medium",
                                    size="2",
                                ),
                            ),
                            rx.text(
                                post_datetime,
                                size="1",
                                color_scheme="gray",
                            ),
                            spacing="0",
                        ),
                        align="center",
                    ),
                    rx.tablet_and_desktop(
                        rx.vstack(
                            rx.text(post.title, size="5", weight="bold"),
                            rx.text(
                                post.content,
                                font_size="1em",
                            ),
                            spacing="3",
                        ),
                    ),
                    rx.mobile_only(
                        rx.vstack(
                            rx.text(post.title, size="3", weight="bold"),
                            rx.text(
                                post.content,
                                font_size="0.9em",
                            ),
                            spacing="1",
                        ),
                    ),
                    direction="column",
                    spacing="4",
                    padding=["1em 0.5em", "1.5em"],
                ),

                rx.separator(
                    margin_bottom="1em",
                ),
                # comments of the post
                comments(
                    post_comments
                ),

                rx.vstack(
                    # form to comment the post
                    write_comment_form(
                        post=post,
                        publish_comment=publish_comment,
                    ),
                    direction="column",
                    spacing="4",
                    padding=["1em 0.5em", "1.5em"],
                ),
                padding=["0em 0em", "0em"],
            ),
        )


post_dialog = PostDialog.create
