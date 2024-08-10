from typing import Callable, Tuple
import reflex as rx

from ..components.comments import comments
from ..components.profile_picture import profile_picture
from ..components.write_comment_form import write_comment_form
from ..models import Comment, Post, UserAccount


class PostDialog(rx.ComponentState):

    @classmethod
    def get_component(cls, **props):
        post: Post = props.pop('post', None)
        post_datetime: str = props.pop('post_datetime', '')
        post_author: UserAccount = props.pop('post_author', None)

        post_comments: list[Tuple[Comment, str, UserAccount]] = (
            props.pop('post_comments', [])
        )
        load_post_details: Callable = props.pop('load_post_details')
        publish_comment: Callable = props.pop('publish_comment')

        return rx.dialog.root(
            rx.dialog.trigger(
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            profile_picture(
                                style=rx.Style(
                                    border='0.5px solid #ccc',
                                    width='2.7em',
                                    height='2.7em',
                                ),
                                profile_picture=post_author.profile_picture,
                            ),
                            rx.vstack(
                                rx.tablet_and_desktop(
                                    rx.hstack(
                                        rx.text(
                                            post_author.first_name,
                                            class_name='desktop-medium-text',
                                        ),
                                        rx.text(
                                            post_author.last_name,
                                            class_name='desktop-medium-text',
                                        ),
                                        spacing='1',
                                    ),
                                ),
                                rx.mobile_only(
                                    rx.hstack(
                                        rx.text(
                                            post_author.first_name,
                                            class_name='mobile-medium-text',
                                        ),
                                        rx.text(
                                            post_author.last_name,
                                            class_name='mobile-medium-text',
                                        ),
                                        spacing='1',
                                    ),
                                ),
                                rx.text(
                                    post_datetime,
                                    class_name='discreet-text',
                                ),
                                spacing='0',
                            ),
                        ),
                        rx.tablet_and_desktop(
                            rx.text(
                                post.title,
                                class_name='desktop-title',
                                margin_bottom='0.5em',
                            ),
                            rx.text(
                                post.content,
                                class_name='desktop-text',
                            ),
                        ),
                        rx.mobile_only(
                            rx.text(
                                post.title,
                                class_name='mobile-title',
                                margin_bottom='0.3em',
                            ),
                            rx.text(
                                post.content,
                                class_name='mobile-text',
                            ),
                        ),
                        width='100%',
                    ),
                    padding=['1em', '1.2em'],
                    cursor='pointer',
                ),
                on_click=load_post_details(post.id)
            ),
            rx.dialog.content(
                rx.flex(
                    rx.hstack(
                        profile_picture(
                            style=rx.Style(
                                border='0.5px solid #ccc',
                                width='2.7em',
                                height='2.7em',
                            ),
                            profile_picture=post_author.profile_picture,
                        ),
                        rx.vstack(
                            rx.tablet_and_desktop(
                                rx.hstack(
                                    rx.text(
                                        post_author.first_name,
                                        style={
                                            'font_weight': '500',
                                        },
                                    ),
                                    rx.text(
                                        post_author.last_name,
                                        style={
                                            'font_weight': '500',
                                        },
                                    ),
                                    spacing='1',
                                ),
                            ),
                            rx.mobile_only(
                                rx.hstack(
                                    rx.text(
                                        post_author.first_name,
                                        style={
                                            'font_weight': '500',
                                            'font_size': '0.9em',
                                        },
                                    ),
                                    rx.text(
                                        post_author.last_name,
                                        style={
                                            'font_weight': '500',
                                            'font_size': '0.9em',
                                        },
                                    ),
                                    spacing='1',
                                ),
                            ),
                            rx.text(
                                post_datetime,
                                style={
                                    'font_size': '0.8em',
                                    'color': 'gray',
                                },
                            ),
                            spacing='0',
                        ),
                    ),
                    rx.tablet_and_desktop(
                        rx.vstack(
                            rx.text(
                                post.title,
                                style={
                                    'font_weight': '700',
                                    'font_size': '1.1em',
                                },
                            ),
                            rx.text(
                                post.content,
                            ),
                            spacing='3',
                        ),
                    ),
                    rx.mobile_only(
                        rx.vstack(
                            rx.text(
                                post.title,
                                style={
                                    'font_weight': '700',
                                    'font_size': '1em',
                                },
                            ),
                            rx.text(
                                post.content,
                                style={
                                    'font_size': '0.9em',
                                },
                            ),
                            spacing='1',
                        ),
                    ),
                    direction='column',
                    spacing='4',
                    padding=['1em 0.5em', '1.5em'],
                ),

                rx.separator(
                    margin_bottom='1em',
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
                    direction='column',
                    spacing='4',
                    padding=['1em 0.5em', '1.5em'],
                ),
                padding=['0em 0em', '0em'],
            ),
        )


post_dialog = PostDialog.create
