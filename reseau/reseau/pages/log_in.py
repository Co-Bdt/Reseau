import asyncio
from collections.abc import AsyncGenerator
import reflex as rx

from ..common.base_state import BaseState
from ..reseau import LOGIN_ROUTE, REGISTER_ROUTE
from ..models import UserAccount
from ..common.template import template


class LogInState(BaseState):
    """Handle login form submission and
    redirect to proper routes after authentication."""

    success: bool = False
    redirect_to: str = ""

    async def on_submit(
            self,
            form_data
    ) -> AsyncGenerator[rx.event.EventSpec |
                        list[rx.event.EventSpec] | None, None]:
        """Handle login form on_submit.

        Args:
            form_data: A dict of form fields and values.
        """
        self.error_message = ""
        username = form_data["username"]
        if not username:
            yield rx.set_focus("username")
            yield rx.toast.error("Le nom d'utilisateur est requis.")
            return
        password = form_data["password"]
        if not password:
            yield rx.set_focus("password")
            yield rx.toast.error("Le mot de passe est requis.")
            return
        with rx.session() as session:
            user = session.exec(
                UserAccount.select().where(UserAccount.username == username)
            ).one_or_none()
        if user is not None and not user.enabled:
            yield rx.set_value("password", "")
            yield rx.toast.error("Ce compte est désactivé.")
            return
        if user is None or not user.verify_password(password):
            yield rx.set_value("password", "")
            yield rx.toast.error("Les identifiants sont incorrects.")
            return
        if (
            user is not None
            and user.id is not None
            # and user.enabled
            and user.verify_password(password)
        ):
            # Set success and mark the user as logged in
            self.success = True
            yield
            self._login(user.id)
        await asyncio.sleep(0.5)
        yield [LogInState.redir(), LogInState.set_success(False)]

    def redir(self) -> rx.event.EventSpec | None:
        """Redirect to the redirect_to route if logged in,
        or to the login page if not."""
        if not self.is_hydrated:
            # wait until after hydration to ensure auth_token is known
            return LogInState.redir()  # type: ignore
        page = LOGIN_ROUTE
        if not self.is_authenticated and page != LOGIN_ROUTE:
            self.redirect_to = page
            return rx.redirect(LOGIN_ROUTE)
        elif page == LOGIN_ROUTE:
            return rx.redirect(self.redirect_to or "/")


@rx.page(route=LOGIN_ROUTE)
@template
def log_in_page() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """
    login_form_desktop_tablet = rx.form(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "Nom d'utilisateur",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    id="username",
                    size="3",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Mot de passe",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    id="password",
                    type="password",
                    size="3",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.button(
                "Se connecter",
                type="submit",
                size="3",
                width="100%",
            ),
            rx.center(
                rx.link(
                    "Pas encore de compte ?",
                    href=REGISTER_ROUTE,
                    width="100%",
                    text_align="center",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            justify="center",
            min_height="85vh",
        ),
        on_submit=LogInState.on_submit
    )

    login_form_mobile = rx.form(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "Nom d'utilisateur",
                    size="2",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    id="username",
                    size="3",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Mot de passe",
                    size="2",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    id="password",
                    type="password",
                    size="3",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.button(
                "Se connecter",
                type="submit",
                size="3",
                width="100%",
                margin_top="1em",
            ),
            rx.center(
                rx.link(
                    "Pas encore de compte ?",
                    href=REGISTER_ROUTE,
                    width="100%",
                    text_align="center",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            justify="center",
            min_height="85vh",
        ),
        on_submit=LogInState.on_submit
    )

    return rx.cond(
            LogInState.is_hydrated,
            rx.box(
                rx.tablet_and_desktop(
                    rx.vstack(
                        login_form_desktop_tablet,
                        rx.cond(  # conditionally show error messages
                            LogInState.success,
                            rx.center(
                                rx.vstack(
                                    rx.spinner(),
                                    rx.text(
                                        "Connexion réussie",
                                        size="3",
                                        weight="medium",
                                    ),
                                    align="center",
                                ),
                                width="100%",
                            ),
                        ),
                        position="absolute",
                        top="50%",
                        left="50%",
                        transform="translateX(-50%) translateY(-50%)",
                    ),
                ),
                rx.mobile_only(
                    rx.vstack(
                        login_form_mobile,
                        rx.cond(  # conditionally show error messages
                            LogInState.success,
                            rx.center(
                                rx.vstack(
                                    rx.spinner(),
                                    rx.text(
                                        "Connexion réussie",
                                        size="3",
                                        weight="medium",
                                    ),
                                    align="center",
                                ),
                                width="100%",
                            ),
                        ),
                        position="absolute",
                        top="50%",
                        left="50%",
                        transform="translateX(-50%) translateY(-50%)",
                        width="80%",
                    ),
                )
            ),
        )


# Will be useful later for futur pages

# def require_login(page: rx.app.ComponentCallable)
# -> rx.app.ComponentCallable:
#     """Decorator to require authentication before rendering a page.

#     If the user is not authenticated, then redirect to the login page.

#     Args:
#         page: The page to wrap.

#     Returns:
#         The wrapped page component.
#     """

#     def protected_page():
#         return rx.fragment(
#             rx.cond(
#                 # type: ignore
#                 BaseState.is_hydrated & BaseState.is_authenticated,
#                 page(),
#                 rx.center(
#                     # When this spinner mounts,
#                     # it will redirect to the login page
#                     rx.spinner(on_mount=LogInState.redir),
#                 ),
#             )
#         )

#     protected_page.__name__ = page.__name__
#     return protected_page
