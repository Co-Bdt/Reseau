from datetime import datetime
import reflex as rx

from ..reseau import HOME_ROUTE
from ..common.base_state import BaseState
from ..components.landing import landing
from ..models.post import Post
from ..common.template import template


class HomeState(BaseState):
    posts_displayed: list[Post] = []  # posts to display

    def run_script(self):
        """Uncomment any one-time script needed for app initialization here."""
        # delete_cities()
        # insert_cities()
        # delete_users()

    def init(self):
        self.load_all_posts()

    def load_all_posts(self):
        self.posts_displayed = []
        with rx.session() as session:
            posts = session.exec(
                Post.select()
                .where(Post.published)
                .order_by(Post.published_at.desc())
            ).all()
        self.posts_displayed = posts

    def publish_post(self, form_data):
        title = form_data["title"]
        content = form_data["content"]
        post = Post(
            title=title,
            content=content,
            author_id=self.authenticated_user.id,
            published_at=Post.format_datetime(datetime.now()),
        )
        with rx.session() as session:
            session.add(post)
            session.commit()

        self.load_all_posts()
        return rx.toast.success("Post publié.")


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
                rx.dialog.root(
                    rx.dialog.trigger(
                        rx.button(
                            "Ecrire un post",
                            width="100%",
                            size="3",
                            variant="outline",
                            color_scheme="gray",
                            radius="large",
                            style={"justify-content": "start"},
                        ),
                    ),
                    rx.dialog.content(
                        rx.dialog.title("Nouveau post"),
                        rx.form.root(
                            rx.flex(
                                rx.input(
                                    name="title",
                                    placeholder="Titre",
                                    width="100%",
                                    size="2",
                                    variant="soft",
                                    style={
                                        "background-color": "white",
                                    },
                                ),
                                rx.input(
                                    name="content",
                                    placeholder="Qu'as-tu en tête ?",
                                    width="100%",
                                    size="2",
                                    variant="soft",
                                    autofocus=True,
                                    style={"background-color": "white"},
                                ),
                                direction="column",
                                spacing="2",
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
                                            "Publier",
                                            type="submit",
                                        ),
                                    ),
                                ),
                                spacing="3",
                                margin_top="16px",
                                justify="end",
                            ),
                            on_submit=HomeState.publish_post,
                        ),
                    ),
                ),
                rx.center(
                    rx.divider(size="3"),
                    width="100%",
                ),
                rx.grid(
                    rx.foreach(
                        HomeState.posts_displayed,
                        lambda post: rx.card(
                            rx.vstack(
                                rx.text(f"{post.title} - {post.published_at}"),
                                rx.text(f"{post.content}"),
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
