import reflex as rx

from ..common.base_state import BaseState
from ..components.profile import profile
from ..reseau import PROFILE_ROUTE
from ..common.template import template
from ..models.user_account import UserAccount


class ProfileState(BaseState):
    profile_text: str = ""  # the user's profile text

    def init(self):
        self.profile_text = self.authenticated_user.profile_text

    def save_profile_text(self) -> rx.event.EventSpec:
        profile_text_cleaned = self.authenticated_user.clean_profile_text(
            self.profile_text
        )

        # Retrieve the authenticated user with its id
        with rx.session() as session:
            user: UserAccount = session.exec(
                UserAccount.select().where(
                    UserAccount.id == self.authenticated_user.id
                )
            ).first()
            user.profile_text = profile_text_cleaned
            session.add(user)
            session.commit()

        # Update the authenticated user's profile text
        self.set_profile_text(profile_text_cleaned)

        return rx.toast.success("Profil mis à jour.")


@rx.page(title="Profil", route=PROFILE_ROUTE, on_load=ProfileState.init)
@template
def profile_page() -> rx.Component:
    return rx.cond(
        ProfileState.is_hydrated,
        rx.vstack(
            profile(
                ProfileState.profile_text,
                ProfileState.set_profile_text,
                ProfileState.save_profile_text
            ),
            rx.center(
                rx.divider(size="3"),
                width="100%",
            ),
            rx.text("Tags..."),
            width="100%",
        ),
    ),
