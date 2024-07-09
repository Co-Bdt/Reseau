import reflex as rx

from ..reseau import LOGIN_ROUTE, REGISTER_ROUTE
from ..models.user_account import UserAccount
from ..components.sidebar import sidebar
from ..base_state import BaseState


class LogInState(BaseState):
    """Handle login form submission and
    redirect to proper routes after authentication."""

    error_message: str = ""
    redirect_to: str = ""

    def on_submit(self, form_data) -> rx.event.EventSpec:
        """Handle login form on_submit.

        Args:
            form_data: A dict of form fields and values.
        """
        self.error_message = ""
        username = form_data["username"]
        password = form_data["password"]
        with rx.session() as session:
            user = session.exec(
                UserAccount.select().where(UserAccount.username == username)
            ).one_or_none()
        if user is not None and not user.enabled:
            self.error_message = "This account is disabled."
            return rx.set_value("password", "")
        if user is None or not user.verify_password(password):
            self.error_message = "Les identifiants sont incorrects."
            return rx.set_value("password", "")
        if (
            user is not None
            and user.id is not None
            # and user.enabled
            and user.verify_password(password)
        ):
            # mark the user as logged in
            self._login(user.id)
        self.error_message = ""
        return LogInState.redir()  # type: ignore

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
def log_in_page() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """
    login_form = rx.form(
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

    return rx.fragment(
        rx.container(
            rx.hstack(
                sidebar(),
                rx.cond(
                    LogInState.is_hydrated,  # type: ignore
                    rx.vstack(
                        rx.cond(  # conditionally show error messages
                            LogInState.error_message != "",
                            rx.text(LogInState.error_message),
                        ),
                        login_form,
                    ),
                ),
                justify="center",
            )
        )
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
