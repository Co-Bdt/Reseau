import datetime
import reflex as rx
from secrets import token_urlsafe
from sqlmodel import select

from ..models.user_account import UserAccount


AUTH_TOKEN_LOCAL_STORAGE_KEY = "_auth_tokens"
DEFAULT_AUTH_SESSION_EXPIRATION_DELTA = datetime.timedelta(days=7)


class BaseState(rx.State):
    # The auth_token is stored in local storage
    # to persist across tab and browser sessions.
    auth_token: str = rx.LocalStorage(name=AUTH_TOKEN_LOCAL_STORAGE_KEY)

    @rx.cached_var
    def authenticated_user(self) -> UserAccount:
        """The currently authenticated user,
        or a dummy user if not authenticated.

        Returns:
            A User instance with id=-1 if not authenticated,
            or the User instance
            corresponding to the currently authenticated user.
        """
        with rx.session() as session:
            result = session.exec(
                select(UserAccount, auth_session_module)
                .where(
                    auth_session_module.session_id == self.auth_token,
                    auth_session_module.expiration >= datetime.datetime.now(
                        datetime.timezone.utc
                    ),
                    UserAccount.id == auth_session_module.user_id,
                )
            ).first()
            if result:
                user, session = result
                return user
        return UserAccount(id=-1)  # type: ignore

    @rx.cached_var
    def is_authenticated(self) -> bool:
        """Whether the current user is authenticated.

        Returns:
            True if the authenticated user has a positive user ID,
            False otherwise.
        """
        return self.authenticated_user.id >= 0

    def generate_auth_token(self) -> str:
        """
        Creates a cryptographically-secure, URL-safe string
        """
        return token_urlsafe(16)

    def do_logout(self) -> None:
        """Destroy AuthSessions associated with the auth_token."""
        with rx.session() as session:
            for auth_session in session.exec(
                auth_session_module.select().where(
                    auth_session_module.session_id == self.auth_token
                )
            ).all():
                session.delete(auth_session)
            session.commit()
        return self.set_auth_token(None)

    def _login(
        self,
        user_id: int,
        expiration_delta:
            datetime.timedelta = DEFAULT_AUTH_SESSION_EXPIRATION_DELTA,
    ) -> None:
        """Create an AuthSession for the given user_id.

        If the auth_token is already associated with an AuthSession, it will be
        logged out first.

        Args:
            user_id: The user ID to associate with the AuthSession.
            expiration_delta: The amount of time before
            the AuthSession expires.
        """
        if self.is_authenticated:
            self.do_logout()
        if user_id < 0:
            return
        # self.auth_token = self.auth_token or self.generate_auth_token()
        self.set_auth_token(self.generate_auth_token())
        with rx.session() as session:
            session.add(
                auth_session_module(  # type: ignore
                    user_id=user_id,
                    session_id=self.auth_token,
                    expiration=datetime.datetime.now(datetime.timezone.utc)
                    + expiration_delta,
                )
            )
            session.commit()
