from datetime import datetime
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..components.landing import landing
from ..components.post_dialog import post_dialog
from ..components.write_post_dialog import write_post_dialog
from ..models import Comment, Post
from ..reseau import HOME_ROUTE


class HomeState(BaseState):
    posts_displayed: list[Post] = []  # posts to display
    post_comments: list[Comment] = []  # comments of a post

    def run_script(self):
        """Uncomment any one-time script needed for app initialization here."""
        # delete_cities()
        # insert_cities()
        # delete_users()
        # insert_interests()

    def init(self):
        # self.run_script()
        self.load_all_posts()

    def load_all_posts(self):
        self.posts_displayed = []
        with rx.session() as session:
            posts = session.exec(
                Post.select().options(
                    sa.orm.selectinload(Post.comment_list)
                )
                .where(Post.published)
                .order_by(Post.published_at.desc())
            ).all()
        self.posts_displayed = posts

    def load_post_comments(self, post_id):
        self.post_comments = []
        with rx.session() as session:
            comments = session.exec(
                Comment.select()
                .where(Comment.post_id == post_id)
                .order_by(Comment.published_at.desc())
            ).all()

        # print("comment_list:", self.posts_displayed[post_id].comment_list)
        self.post_comments = comments

    def publish_post(self, form_data: dict):
        title = form_data["title"]
        content = form_data["content"]
        post = Post(
            title=title,
            content=content,
            user_account_id=self.authenticated_user.id,
            published_at=Post.format_datetime(datetime.now()),
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
            published_at=Comment.format_datetime(datetime.now()),
        )
        with rx.session() as session:
            session.add(comment)
            session.commit()

        self.load_post_comments(post_id)
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
        # rx.color_mode.button(position="top-right"),
        rx.cond(
            BaseState.is_authenticated,
            rx.vstack(
                write_post_dialog(HomeState.publish_post),
                rx.center(
                    rx.divider(size="3"),
                    width="100%",
                ),
                rx.grid(
                    rx.foreach(
                        HomeState.posts_displayed,
                        lambda post: rx.card(
                            post_dialog(
                                post=post,
                                post_comments=HomeState.post_comments,
                                load_comments=HomeState.load_post_comments,
                                publish_comment=HomeState.publish_comment,
                            ),
                            as_child=True,
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
            ),
        ),
    )
