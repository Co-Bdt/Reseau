import os
from random import shuffle
from typing import Tuple
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..components.user_card import user_card
from ..models import City, Interest, UserAccount, UserInterest
from ..reseau import MEMBERS_ROUTE


class MembersState(BaseState):
    # users with their city to display
    users_displayed: list[Tuple[UserAccount, bool, City, list[Interest]]] = []
    search_term: str = ""  # the term typed in the search bar
    city_searched: City = None  # the first city detected with the search term

    def init(self):
        self.load_users()

    def load_users(self):
        self.users_displayed = []
        with rx.session() as session:
            users = session.exec(
                UserAccount.select()
                .options(
                    sa.orm.selectinload(UserAccount.city),
                    sa.orm.selectinload(
                        UserAccount.interest_list
                    ).selectinload(UserInterest.interest)
                )
            ).all()

        for user in users:
            if user.id != self.authenticated_user.id:
                user_interest_names: list[Interest] = []
                for interest in user.interest_list:
                    user_interest_names.append(interest.interest)
                self.users_displayed.append(
                    (user,
                     os.path.isfile(f"{rx.get_upload_dir()}/{user.id}" +
                                    "_profile_picture.png"),
                     user.city,
                     user_interest_names)
                )

        # Display users in random order.
        shuffle(self.users_displayed)

    def search_city(self, form_data):
        self.search_term = form_data["search_term"]

        # If no search term, display all users.
        if not self.search_term:
            return self.load_users()

        # Fetch the first city matching the search term.
        with rx.session() as session:
            city: City = session.exec(
                City.select().where(
                    sa.func.lower(City.name).startswith(
                        sa.func.lower(self.search_term)
                    )
                )
            ).first()
        # Fetch the users living in the city.
        users = []
        if city is not None:
            users = session.exec(
                UserAccount.select().where(UserAccount.city_id == city.id)
            ).all()
            self.city_searched = city

        self.users_displayed.clear()
        for user in users:
            self.users_displayed.append((user, city))


@rx.page(title="Membres", route=MEMBERS_ROUTE, on_load=MembersState.init)
@template
def members_page() -> rx.Component:
    """
    Render the members page which allow users \
        to search for other users by city.

    Returns:
        A reflex component.
    """
    return rx.cond(
        MembersState.is_hydrated,
        rx.vstack(
            rx.form(
                rx.input(
                    id="search_term",
                    placeholder="Rechercher une ville",
                    width="100%",
                    size="3",
                    variant="surface",
                ),
                on_submit=MembersState.search_city,
            ),
            # display all users by default
            # else display the users in the city searched
            # or a message if no user is found
            rx.cond(
                MembersState.users_displayed,
                rx.grid(
                    rx.foreach(
                        MembersState.users_displayed,
                        lambda user: user_card(
                            user=(user[0], user[1]),
                            city=user[2],
                            interest_list=user[3],
                            is_profile_empty=~user[0].profile_text,
                        ),
                    ),
                    columns="3",
                    width="100%",
                    spacing="3",
                    flex_wrap="wrap",
                ),
                rx.cond(
                    MembersState.city_searched,
                    rx.text(
                        f"Aucune personne trouvée : \
                            {MembersState.city_searched.name} \
                            ({MembersState.city_searched.postal_code})",
                        width="100%",
                        align="center",
                    ),
                    rx.center(
                        rx.spinner(),
                        width="100%",
                    ),
                ),
            ),
        ),
    )
