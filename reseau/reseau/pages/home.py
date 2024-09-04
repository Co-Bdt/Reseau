from datetime import datetime
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..common.translate import from_now
from ..components.landing import landing_page
from ..components.postcategory_badges import postcategory_badges
from ..components.post_dialog import post_dialog
from ..components.write_post_dialog import write_post_dialog
from ..models import Comment, Post, PostCategory, UserAccount
from ..reseau import DEFAULT_POSTCATEGORY, HOME_ROUTE
from ..scripts.load_profile_pictures import load_profile_pictures


class HomeState(BaseState):
    last_users: list[UserAccount] = []  # 2 last users created
    # posts to display
    posts_displayed: list[tuple[Post, str, UserAccount, int]] = []
    post_author: UserAccount = None  # author of a post
    # comments of a post
    post_comments: list[tuple[Comment, str, UserAccount]] = []
    postcategories: tuple[list[PostCategory], list[str]] = ()

    def run_script(self):
        '''Uncomment any one-time script needed for app initialization here.'''
        # delete_cities()
        # insert_cities()
        # delete_users()
        # insert_interests()
        load_profile_pictures()

    def init(self):
        self.run_script()
        self.load_last_users()
        self.load_posts(DEFAULT_POSTCATEGORY)
        self.load_postcategories()

    def load_last_users(self):
        with rx.session() as session:
            self.last_users = session.exec(
                UserAccount.select().options(
                    sa.orm.selectinload(UserAccount.city),
                )
                .order_by(UserAccount.id.desc())
                .limit(2)
            ).all()

    def load_posts(self, postcategory_id: int):
        self.posts_displayed = []
        # filter_by_category = True if postcategory_id != 0 else False

        with rx.session() as session:
            posts = session.exec(
                Post.select().options(
                    sa.orm.selectinload(Post.useraccount)
                    .selectinload(UserAccount.city),
                    sa.orm.selectinload(Post.comment_list),
                )
                .where(
                    Post.is_published
                )
                .order_by(Post.published_at.desc())
            ).all()

        # Keep only the posts of the selected category
        if (postcategory_id != 0):
            posts = [
                post for post in posts if post.category_id == postcategory_id
            ]

        # Put pinned posts at the top
        pinned_posts = [post for post in posts if post.is_pinned]
        other_posts = [post for post in posts if not post.is_pinned]
        posts = pinned_posts + other_posts

        for post in posts:
            self.posts_displayed.append(
                (post,
                 from_now(post.published_at),
                 post.useraccount,
                 len(post.comment_list)),
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
                 from_now(comment.published_at),
                 comment.useraccount),
            )

    def load_postcategories(self):
        self.postcategories = []
        postcategories_as_str = []

        with rx.session() as session:
            postcategories = session.exec(
                PostCategory.select()
            ).all()
        for postcategory in postcategories:
            postcategories_as_str.append(postcategory.name)
        self.postcategories = (postcategories, postcategories_as_str)

    def publish_post(self, form_data: dict):
        title = form_data['title']
        content = form_data['content']
        category = form_data['category']
        print(category)

        if not content:
            return rx.toast.warning("Ton post doit avoir un contenu.")

        category_id = DEFAULT_POSTCATEGORY
        # for postcategory in HomeState.postcategories[0]:
        #     if postcategory.name == category:
        #         category_id = postcategory.id
        #         print(category_id)
        #         break

        post = Post(
            title=title,
            content=content,
            author_id=self.authenticated_user.id,
            category_id=category_id,
            published_at=datetime.now(),
        )
        # with rx.session() as session:
        #     session.add(post)
        #     session.commit()

        self.load_posts(DEFAULT_POSTCATEGORY)

        return rx.toast.success("Post publié.")

    def publish_comment(self, form_data: dict):
        if not form_data['content']:
            return rx.toast.warning("Ton commentaire est vide.")

        post_id = form_data['post_id']
        comment = Comment(
            content=form_data['content'],
            post_id=post_id,
            author_id=self.authenticated_user.id,
            published_at=datetime.now(),
        )
        with rx.session() as session:
            session.add(comment)
            session.commit()

        self.load_post_details(post_id)
        return rx.toast.success("Commentaire publié.")


@rx.page(title='Reseau', route=HOME_ROUTE, on_load=HomeState.init)
@template
def home_page() -> rx.Component:
    '''Render the landing page for visitors, \
        or the home page for authenticated users.

    Returns:
        A reflex component.
    '''
    return rx.cond(
        HomeState.is_hydrated,
        rx.cond(
            HomeState.is_authenticated,
            rx.vstack(
                write_post_dialog(
                    user=HomeState.authenticated_user,
                    postcategories=HomeState.postcategories[1],
                    publish_post=HomeState.publish_post
                ),
                postcategory_badges(
                    postcategories=HomeState.postcategories[0],
                ),
                rx.grid(
                    rx.foreach(
                        HomeState.posts_displayed,
                        lambda post:
                            post_dialog(
                                post=post[0],
                                post_datetime=post[1],
                                post_author=post[2],
                                post_comments_count=post[3],
                                post_comments=HomeState.post_comments,
                                load_post_details=HomeState.load_post_details,
                                publish_comment=HomeState.publish_comment,
                            ),
                    ),
                    columns='1',
                    width='100%',
                    spacing='3',
                ),
                width='100%',
            ),
            rx.box(
                landing_page(
                    last_users=HomeState.last_users,
                ),
                position='absolute',
                top='50%',
                left='50%',
                transform='translateX(-50%) translateY(-50%)',
                width=['80%', '80%', '70%', '60%', '50%'],
            ),
        ),
    )
