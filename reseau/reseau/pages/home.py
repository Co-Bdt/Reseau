import reflex as rx
from random import shuffle
from sqlalchemy import func
from typing import Tuple

from ..reseau import HOME_ROUTE
from ..base_state import BaseState
from ..components.user_card import user_card
from ..components.landing import landing
from ..components.sidebar import sidebar
from ..components.profile import profile
from ..models.user_account import UserAccount
from ..models.city import City


class HomeState(BaseState):
    profile_text: str = ""  # the user's profile text
    users_displayed: list[Tuple[UserAccount, City]] = []  # users to display
    search_term: str = ""  # the term typed in the search bar
    city_searched: City = None  # the first city detected with the search term

    def run_script(self):
        """Uncomment any one-time script needed for app initialization here."""
        # delete_cities()
        # insert_cities()
        # delete_users()

    def init_home(self):
        self.profile_text = self.authenticated_user.profile_text
        self.load_all_users()

    def load_all_users(self):
        self.users_displayed = []
        with rx.session() as session:
            users = session.exec(UserAccount.select()).all()

        for user in users:
            city = session.exec(
                City.select().where(City.id == user.city)
            ).first()
            self.users_displayed.append((user, city))

        shuffle(self.users_displayed)

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

    def search_city(self, form_data):
        self.search_term = form_data["search_term"]

        # If no search term, display all users.
        if not self.search_term:
            return self.load_all_users()

        # Fetch the first city matching the search term.
        with rx.session() as session:
            city: City = session.exec(
                City.select().where(
                    func.lower(City.name).startswith(
                        func.lower(self.search_term)
                    )
                )
            ).first()
        # Fetch the users living in the city.
        users = []
        if city is not None:
            users = session.exec(
                UserAccount.select().where(UserAccount.city == city.id)
            ).all()
            self.city_searched = city

        self.users_displayed.clear()
        for user in users:
            self.users_displayed.append((user, city))


@rx.page(title="Reseau", route=HOME_ROUTE, on_load=HomeState.init_home)
def home_page() -> rx.Component:
    home = rx.vstack(
        rx.vstack(
            rx.desktop_only(
                rx.center(
                    rx.heading(
                        "Rɘseau",
                        size="8",
                        style={
                            "font-family": "Droid Sans Mono",
                            "letter-spacing": "1px"
                        },
                    ),
                    width="100%",
                    margin="0 0 3em 0",
                ),
                width="100%",
            ),
            rx.mobile_and_tablet(
                rx.box(
                    rx.heading(
                        "Rɘseau",
                        size="8",
                        style={
                            "font-family": "Droid Sans Mono",
                            "letter-spacing": "1px"
                        },
                    ),
                    width="100%",
                    justify="start",
                    margin="0 0 3em 0.5em",
                ),
            ),
            profile(
                HomeState.profile_text,
                HomeState.set_profile_text,
                HomeState.save_profile_text),
            width="100%",
        ),
        rx.center(
            rx.divider(size="3"),
            width="100%",
        ),
        rx.form(
            rx.input(
                id="search_term",
                placeholder="Rechercher une ville",
                width="100%",
                size="3",
                variant="surface",
            ),
            on_submit=HomeState.search_city,
        ),
        # display all users by default
        # else display the users in the city searched
        # or a message if no user is found
        rx.cond(
            HomeState.users_displayed,
            rx.flex(
                rx.foreach(
                    HomeState.users_displayed,
                    lambda user: user_card(
                        user[0],
                        user[1],
                        ~user[0].profile_text,),
                ),
                width="100%",
                direction="row",
                spacing="3",
                flex_wrap="wrap",
            ),
            rx.cond(
                HomeState.city_searched,
                rx.text(
                    f"Aucune personne trouvée : \
                        {HomeState.city_searched.name} \
                        ({HomeState.city_searched.postal_code})",
                    width="100%",
                    align="center",
                ),
                rx.center(
                    rx.spinner(),
                    width="100%",
                ),
            ),
        ),
        width="100%",
        justify="center",
        spacing="5",
    )

    return rx.box(
        # toggle dark/light mode using right top corner button
        # rx.color_mode.button(position="top-right"),
        rx.cond(
            BaseState.is_authenticated,
            rx.box(
                sidebar(),
                rx.box(
                    home,
                    margin=["12px", "12px", "12px", "4em 8em"],
                )
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
