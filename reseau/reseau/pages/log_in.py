import asyncio
from collections.abc import AsyncGenerator
import reflex as rx

from ..common.base_state import BaseState
from ..common.template import template
from ..components.custom.react_oauth_google import GoogleLogin
from ..components.custom.react_oauth_google import GoogleOAuthProvider
from ..components.registration.registration_account_step import RegistrationAccountStepState  # noqa: E501
from ..models import UserAccount
from ..reseau import LOGIN_ROUTE, REGISTER_ROUTE, GOOGLE_AUTH_CLIENT_ID


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
        email = form_data["email"]
        if not email:
            yield rx.set_focus("email")
            yield rx.toast.error("Ton email est requis.")
            return
        password = form_data["password"]
        if not password:
            yield rx.set_focus("password")
            yield rx.toast.error("Ton mot de passe est requis.")
            return
        with rx.session() as session:
            user = session.exec(
                UserAccount.select().where(UserAccount.email == email)
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
            and user.enabled
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
    login_form = rx.form(
        rx.vstack(
            rx.text(
                "Se connecter à Reseau",
                font_weight='700',
                font_size='1.75em',
                font_family='Inter, sans-serif',
                style=rx.Style(
                    margin_bottom='0.75em',
                ),
            ),
            rx.input(
                id='email',
                placeholder='Email',
                size='3',
                width='20em',
            ),
            rx.input(
                id='password',
                placeholder='Mot de passe',
                type='password',
                size='3',
                width='20em',
            ),

            rx.button(
                "Se connecter",
                type='submit',
                size='3',
                width='20em',
                margin_top='1em',
            ),
            rx.center(
                rx.link(
                    "Pas encore de compte ?",
                    href=REGISTER_ROUTE,
                ),
                direction='column',
                spacing='5',
                width='100%',
            ),

            rx.center(
                rx.hstack(
                    rx.divider(
                        size='3',
                        width='100%',
                    ),
                    rx.text(
                        "ou",
                        style=rx.Style(
                            color='#64748B',
                            font_size='0.9em',
                            font_family='Inter, sans-serif',
                        ),
                    ),
                    rx.divider(
                        size='3',
                        width='100%',
                    ),
                    width='100%',
                ),
                width='100%',
                margin_y='0.5em',
            ),
            rx.box(
                GoogleOAuthProvider.create(
                    GoogleLogin.create(
                        text='signin_with',
                        on_success=RegistrationAccountStepState.on_google_auth_success  # noqa: E501
                    ),
                    client_id=GOOGLE_AUTH_CLIENT_ID,
                ),
                style=rx.Style(
                    align_self='center',
                ),
            ),
            justify='center',
        ),
        on_submit=LogInState.on_submit,
        padding_x='3.5em',
        padding_y='3em',
        border='1px solid #E3E4EB',
        border_radius='0.75em',
        box_shadow='0px 3px 4px 1px rgba(0, 0, 0, 0.05)',
    )

    return rx.cond(
        LogInState.is_hydrated,
        rx.box(
            rx.vstack(
                login_form,
                rx.cond(  # Conditionally show success messages
                    LogInState.success,
                    rx.center(
                        rx.vstack(
                            rx.spinner(),
                            rx.text(
                                "Connexion réussie",
                                size='3',
                                weight='medium',
                            ),
                            align='center',
                        ),
                        width='100%',
                    ),
                    # This is a placeholder for the success message
                    # to always takes the space.
                    rx.vstack(
                        rx.spinner(
                            visibility='hidden',
                        ),
                        rx.text(
                            "Connexion réussie",
                            size='3',
                            weight='medium',
                            visibility='hidden',
                        ),
                    ),
                ),
                position='absolute',
                top='50%',
                left='50%',
                transform='translateX(-50%) translateY(-50%)',
            ),
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
