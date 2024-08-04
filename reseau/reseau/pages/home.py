from datetime import datetime
import os
import reflex as rx
import sqlalchemy as sa
from typing import Tuple

from ..common.base_state import BaseState
from ..common.template import template
from ..components.landing import landing
from ..components.post_dialog import post_dialog
from ..components.write_post_dialog import write_post_dialog
from ..models import Comment, Post, UserAccount
from ..reseau import HOME_ROUTE


class HomeState(BaseState):
    # if current user has a profile picture
    own_profile_picture_exists: bool = False
    # posts to display
    posts_displayed: list[Tuple[Post, str, UserAccount, bool]] = []
    post_author: UserAccount = None  # author of a post
    # comments of a post
    post_comments: list[Tuple[Comment, str, UserAccount, bool]] = []
    profile_pictures_exist: list[bool] = []

    def run_script(self):
        """Uncomment any one-time script needed for app initialization here."""
        # delete_cities()
        # insert_cities()
        # delete_users()
        # insert_interests()

    def init(self):
        # self.run_script()
        self.own_profile_picture_exists = os.path.isfile(
            f"{rx.get_upload_dir()}/{self.authenticated_user.id}" +
            "_profile_picture.png"
        )
        self.load_all_posts()

    def load_all_posts(self):
        self.posts_displayed = []
        with rx.session() as session:
            posts = session.exec(
                Post.select().options(
                    sa.orm.selectinload(Post.useraccount),
                    sa.orm.selectinload(Post.comment_list),
                )
                .where(Post.published)
                .order_by(Post.published_at.desc())
            ).all()

        for post in posts:
            self.posts_displayed.append(
                (post,
                 f"{post.published_at: %d/%m/%y %H:%M}",
                 post.useraccount,
                 os.path.isfile(f"{rx.get_upload_dir()}/{post.author_id}" +
                                "_profile_picture.png")),
            )

    def load_post_details(self, post_id: int):
        self.post_author = None
        self.post_comments = []

        with rx.session() as session:
            comments = session.exec(
                Comment.select()
                .options(sa.orm.selectinload(Comment.useraccount))
                .where(Comment.post_id == post_id)
                .order_by(Comment.published_at.asc())
            ).all()
        for comment in comments:
            self.post_comments.append(
                (comment,
                 f"{comment.published_at: %d/%m/%y %H:%M}",
                 comment.useraccount,
                 os.path.isfile(f"{rx.get_upload_dir()}/{comment.author_id}" +
                                "_profile_picture.png")),
            )

    def publish_post(self, form_data: dict):
        title = form_data["title"]
        content = form_data["content"]

        if not content:
            return rx.toast.warning("Ton post doit avoir un contenu.")

        post = Post(
            title=title,
            content=content,
            author_id=self.authenticated_user.id,
            published_at=datetime.now(),
        )
        with rx.session() as session:
            session.add(post)
            session.commit()

        self.load_all_posts()

        return rx.toast.success("Post publié.")

    def publish_comment(self, form_data: dict):
        post_id = form_data["post_id"]
        comment = Comment(
            content=form_data["content"],
            post_id=post_id,
            author_id=self.authenticated_user.id,
            published_at=datetime.now(),
        )
        with rx.session() as session:
            session.add(comment)
            session.commit()

        self.load_post_details(post_id)
        return rx.toast.success("Commentaire publié.")


@rx.page(title="Reseau", route=HOME_ROUTE, on_load=HomeState.init)
@template
def home_page() -> rx.Component:
    """Render the landing page for visitors, \
        or the home page for authenticated users.

    Returns:
        A reflex component.
    """
    return rx.cond(
        HomeState.is_hydrated,
        # toggle dark/light mode using right top corner button
        # can't work while icons stay black
        rx.cond(
            BaseState.is_authenticated,
            rx.vstack(
                rx.heading(
                    "Communauté",
                    size="5",
                    style=rx.Style(
                        margin_bottom="0.5em"
                    ),
                ),
                write_post_dialog(
                    user=[BaseState.authenticated_user,
                          HomeState.own_profile_picture_exists],
                    publish_post=HomeState.publish_post
                ),
                rx.tablet_and_desktop(
                    rx.spacer(spacing="2"),
                ),
                rx.grid(
                    rx.foreach(
                        HomeState.posts_displayed,
                        lambda post:
                            post_dialog(
                                post=post[0],
                                post_datetime=post[1],
                                post_author=post[2],
                                post_profile_picture_exist=post[3],
                                post_comments=HomeState.post_comments,
                                profile_pictures_exist=HomeState.profile_pictures_exist,  # noqa
                                load_post_details=HomeState.load_post_details,
                                publish_comment=HomeState.publish_comment,
                            ),
                    ),
                    columns="1",
                    width="100%",
                    spacing="3",
                ),
                width="100%",
            ),
            rx.box(
                landing(),
                position="absolute",
                top="50%",
                left="50%",
                transform="translateX(-50%) translateY(-50%)",
                width=["80%", "80%", "70%", "60%", "50%"],
                # padding_x=["1em", "1em", "1em", "1em", "0"],
            ),
        ),
    )
