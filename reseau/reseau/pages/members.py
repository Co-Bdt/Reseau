from random import shuffle
from typing import Tuple
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..components.members_grid import members_grid
from ..models import City, Interest, UserAccount, UserInterest
from ..reseau import MEMBERS_ROUTE


class MembersState(rx.State):
    # users with their city to display
    users_displayed: list[Tuple[UserAccount, City, list[Interest]]] = []
    search_term: str = ''  # the term typed in the search bar
    city_found: City = None  # the first city found with the search term

    async def init(self):
        await self.load_users()

    async def load_users(self):
        self.users_displayed = []
        base_state = await self.get_state(BaseState)

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
            if user.id != base_state.authenticated_user.id:
                user_interest: list[Interest] = []
                for interest in user.interest_list:
                    user_interest.append(interest.interest)
                self.users_displayed.append(
                    (user,
                     user.city,
                     user_interest)
                )

        # Display users in random order.
        shuffle(self.users_displayed)

    async def search_city(self, form_data):
        self.search_term = form_data["search_term"]
        city: City = None
        base_state = await self.get_state(BaseState)

        # If no search term, display all users.
        if not self.search_term:
            await self.load_users()
            return

        # Clear state variables.
        self.users_displayed.clear()
        self.city_found = None

        # Fetch the first city matching the search term.
        with rx.session() as session:
            city = session.exec(
                City.select()
                .options(
                    sa.orm.selectinload(City.useraccount_list).selectinload(
                        UserAccount.interest_list).selectinload(
                            UserInterest.interest
                        ),
                )
                .where(
                    sa.func.lower(City.name).startswith(
                        sa.func.lower(self.search_term)
                    )
                )
            ).first()

        if city is not None:
            self.city_found = city
            self.users_displayed.clear()
            for user in city.useraccount_list:
                if user.id != base_state.authenticated_user.id:
                    user_interest: list[Interest] = []
                    for interest in user.interest_list:
                        user_interest.append(interest.interest)
                    self.users_displayed.append(
                        (user,
                         city,
                         user_interest)
                    )
        # If no city is found, try to find users with their first or last name.
        else:
            await self.search_user(form_data)

        if self.users_displayed:
            # If found, display users in random order.
            shuffle(self.users_displayed)
        else:
            # Else if no user found.
            if not self.city_found:
                self.city_found = City(
                    name=self.search_term,
                    postal_code="00000"
                )

    async def search_user(self, form_data):
        self.search_term = form_data["search_term"]
        users: list[UserAccount] = []
        base_state = await self.get_state(BaseState)

        # Search first by first name.
        with rx.session() as session:
            users = session.exec(
                UserAccount.select()
                .options(
                    sa.orm.selectinload(UserAccount.city),
                    sa.orm.selectinload(UserAccount.interest_list)
                    .selectinload(UserInterest.interest)
                )
                .where(
                    sa.func.lower(UserAccount.first_name).startswith(
                        sa.func.lower(self.search_term)
                    )
                )
            ).all()

        # Search then by last name if no user is found.
        if not users:
            with rx.session() as session:
                users = session.exec(
                    UserAccount.select()
                    .options(
                        sa.orm.selectinload(UserAccount.city),
                        sa.orm.selectinload(UserAccount.interest_list)
                        .selectinload(UserInterest.interest)
                    )
                    .where(
                        sa.func.lower(UserAccount.last_name).startswith(
                            sa.func.lower(self.search_term)
                        )
                    )
                ).all()

        if users:
            self.users_displayed.clear()
            for user in users:
                if user.id != base_state.authenticated_user.id:
                    user_interest: list[Interest] = []
                    for interest in user.interest_list:
                        user_interest.append(interest.interest)
                    self.users_displayed.append(
                        (user,
                         user.city,
                         user_interest)
                    )


@rx.page(title="Membres", route=MEMBERS_ROUTE, on_load=MembersState.init)
@template
def members_page() -> rx.Component:
    """
    Render the members page which allow users to \
        - search for other users by city or first name
        - start a private discussion with a user

    Returns:
        A reflex component.
    """
    return rx.cond(
        MembersState.is_hydrated,
        rx.vstack(
            rx.form(
                rx.input(
                    id="search_term",
                    placeholder="Recherche une ville ou un membre",
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
                rx.box(
                    rx.desktop_only(
                        members_grid(
                            users=MembersState.users_displayed,
                            columns="3",
                        ),
                    ),
                    rx.tablet_only(
                        members_grid(
                            users=MembersState.users_displayed,
                            columns="2",
                        ),
                    ),
                    rx.mobile_only(
                        members_grid(
                            users=MembersState.users_displayed,
                            columns="1",
                        ),
                    ),
                    width="100%",
                ),
                rx.cond(
                    MembersState.city_found,
                    rx.text(
                        f"Aucun membre trouvé : "
                        f"{MembersState.city_found.name} ",
                        f"({MembersState.city_found.postal_code})",
                        class_name="mobile-text",
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
