from typing import Callable, Tuple
import reflex as rx

from ..components.comments import comments
from ..components.profile_picture import profile_picture
from ..components.write_comment_form import write_comment_form
from ..models import Comment, Post, UserAccount


comment_text_style = {
    'style': rx.Style(
        overflow='hidden',
        text_overflow='break-word',
        max_height='3em',
    ),
}


def post_dialog(**props):
    post: Post = props.pop('post', None)
    post_datetime: str = props.pop('post_datetime', '')
    post_author: UserAccount = props.pop('post_author', None)
    post_comments_count: int = props.pop('post_comments_count', 0)

    post_comments: list[Tuple[Comment, str, UserAccount]] = (
        props.pop('post_comments', [])
    )
    load_post_details: Callable = props.pop('load_post_details')
    publish_comment: Callable = props.pop('publish_comment')

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.card(
                rx.cond(
                    post.is_pinned,
                    rx.box(
                        rx.hstack(
                            rx.icon(
                                tag='pin',
                                color='black',
                                size=16,
                            ),
                            rx.text(
                                "Épinglé",
                                style={
                                    'color': 'black',
                                    'font_size': '0.8em',
                                    'font_weight': '600',
                                },
                            ),
                            spacing='2',
                        ),
                        width='100%',
                        background_color=rx.color_mode_cond(
                            '#FFC53D',
                            '#E4B037'
                        ),
                        padding_x='0.8em',
                        padding_y='0.5em',
                    ),
                ),
                rx.vstack(
                    rx.hstack(
                        profile_picture(
                            style=rx.Style(
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
                                        style=rx.Style(
                                            font_weight='600',
                                        ),
                                    ),
                                    rx.text(
                                        post_author.last_name,
                                        style=rx.Style(
                                            font_weight='600',
                                        ),
                                    ),
                                    spacing='1',
                                ),
                            ),
                            rx.mobile_only(
                                rx.hstack(
                                    rx.text(
                                        post_author.first_name,
                                        style=rx.Style(
                                            font_weight='600',
                                            font_size='0.9em',
                                        ),
                                    ),
                                    rx.text(
                                        post_author.last_name,
                                        style=rx.Style(
                                            font_weight='600',
                                            font_size='0.9em',
                                        ),
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
                            style=rx.Style(
                                font_weight='700',
                                font_size='1.2em',
                                margin_bottom='0.5em',
                            ),
                        ),
                        rx.box(
                            post.content,
                            class_name='desktop-text',
                            **comment_text_style,
                        ),
                    ),
                    rx.mobile_only(
                        rx.text(
                            post.title,
                            style=rx.Style(
                                font_weight='700',
                                font_size='1.1em',
                                margin_bottom='0.3em',
                            ),
                        ),
                        rx.box(
                            post.content,
                            class_name='mobile-text',
                            **comment_text_style,
                        ),
                    ),
                    rx.cond(
                        post_comments_count > 0,
                        rx.text(
                            f"{post_comments_count} commentaire(s)",
                            class_name='discreet-text',
                        ),
                        rx.text(
                            "Sois le premier à commenter",
                            class_name='discreet-text',
                        )
                    ),
                    width='100%',
                    padding=['1em', '1.2em'],
                ),
                padding='0',
                cursor='pointer',
                style={
                    '_hover': {
                        'box_shadow': '0px 1px 3px 1px rgba(0, 0, 0, 0.2)',
                    },
                },
            ),
            on_click=load_post_details(post.id)
        ),
        rx.dialog.content(
            rx.flex(
                rx.hstack(
                    profile_picture(
                        style=rx.Style(
                            width='2.7em',
                            height='2.7em',
                        ),
                        profile_picture=post_author.profile_picture,
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text(
                                post_author.first_name,
                                style=rx.Style(
                                    font_family='Satoshi, sans-serif',
                                    font_weight='600',
                                ),
                            ),
                            rx.text(
                                post_author.last_name,
                                style=rx.Style(
                                    font_family='Satoshi, sans-serif',
                                    font_weight='600',
                                ),
                            ),
                            spacing='1',
                        ),
                        rx.text(
                            post_datetime,
                            style=rx.Style(
                                color='gray',
                                font_family='Satoshi, sans-serif',
                                font_size='0.8em',
                            ),
                        ),
                        spacing='0',
                    ),
                ),
                rx.vstack(
                    rx.text(
                        post.title,
                        style=rx.Style(
                            font_family='Satoshi, sans-serif',
                            font_weight='700',
                            font_size=['1.3em', '1.4em'],
                        ),
                    ),
                    rx.text(
                        f"{post.content}",
                        style=rx.Style(
                            font_family='Satoshi, sans-serif',
                            font_size=['0.9em', '1em'],
                            white_space='pre-wrap',
                        ),
                    ),
                    spacing='3',
                ),
                direction='column',
                spacing='4',
                padding=['1em', '1.5em'],
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
                padding=['1em', '1.5em'],
            ),
            padding='0em',
            max_width=['95%', '90%', '75%', '60%', '50%'],
        ),
    )
