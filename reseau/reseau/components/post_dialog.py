import reflex as rx

from ..models.user_account import Comment, Post


class PostDialog(rx.ComponentState):
    post: Post = None
    post_comments: list[Comment] = []
    comment_value: str = ""

    @classmethod
    def get_component(cls, **props):
        cls.post = props.pop("post")
        cls.post_comments = props.pop("post_comments")
        load_comments = props.pop("load_comments")
        publish_comment = props.pop("publish_comment")

        return rx.dialog.root(
            rx.dialog.trigger(
                rx.card(
                    rx.text(
                        f"{cls.post.title} - \
                            {cls.post.published_at}"
                    ),
                    rx.text(f"{cls.post.content}"),
                    width="100%",
                ),
                on_click=load_comments(cls.post.id)
            ),
            rx.dialog.content(
                rx.dialog.title(cls.post.title),
                rx.flex(
                    rx.text(f"{cls.post.published_at}"),
                    rx.text(f"{cls.post.content}"),

                    # comments of the post
                    rx.text("Commentaires", size="4", font_weight="bold"),
                    rx.grid(
                        rx.foreach(
                            cls.post_comments,
                            lambda comment: rx.card(
                                rx.text(
                                    comment.published_at,
                                ),
                                rx.text(f"{comment.content}"),
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
                            value=cls.post.id,
                            style=rx.Style(display="none"),
                        ),
                        rx.input(
                            name="content",
                            placeholder="Commente...",
                            value=cls.comment_value,
                            on_change=cls.set_comment_value,
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
                    ),
                    direction="column",
                    spacing="2",
                ),
            ),
        )


post_dialog = PostDialog.create
