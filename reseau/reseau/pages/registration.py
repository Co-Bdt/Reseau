from __future__ import annotations
import asyncio
from collections.abc import AsyncGenerator
from re import match
import reflex as rx
from unidecode import unidecode

from ..reseau import REGISTER_ROUTE

from ..models.city import City
from ..components.sidebar import sidebar
from ..base_state import BaseState
from .log_in import LOGIN_ROUTE
from ..models.user_account import UserAccount


class RegistrationState(BaseState):
    """Handle registration form submission and
    redirect to login page after registration."""

    success: bool = False
    error_message: str = ""

    cities_as_str: list[str] = []

    def load_cities(self):
        """Load cities from the database."""
        with rx.session() as session:
            cities = session.exec(
                City.select().order_by(City.name)
            ).all()
        self.cities_as_str = [f"{unidecode(city.name)} ({city.postal_code})"
                              for city in cities]
        self.cities_as_str = sorted(self.cities_as_str)

    async def handle_registration(
        self, form_data
    ) -> AsyncGenerator[rx.event.EventSpec |
                        list[rx.event.EventSpec] | None, None]:
        """Handle registration form on_submit.

        Set error_message appropriately based on validation results.

        Args:
            form_data: A dict of form fields and values.
        """
        with rx.session() as session:
            username = form_data["username"]
            if not username:
                self.error_message = "Le nom ne peut pas être vide."
                yield rx.set_focus("username")
                return
            existing_user = session.exec(
                UserAccount.select().where(UserAccount.username == username)
            ).one_or_none()
            if existing_user is not None:
                self.error_message = (
                    f"Le nom {username} est déjà utilisé. \
                        Essaye-en un autre."
                )
                yield [rx.set_value("username", ""), rx.set_focus("username")]
                return
            email = form_data["email"]
            if not email:
                self.error_message = "L'email ne peut pas être vide."
                yield rx.set_focus("email")
                return
            # Define a regex pattern for validating the email
            pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            # Use the re package to check if the email matches the pattern
            if not match(pattern, email):
                self.error_message = "L'email n'est pas valide."
                yield rx.set_focus("email")
                return
            password = form_data["password"]
            if not password:
                self.error_message = "Le mot de passe ne peut pas être vide."
                yield rx.set_focus("password")
                return
            if password != form_data["confirm_password"]:
                self.error_message = "Les mots de passe ne correspondent pas."
                yield [
                    rx.set_value("confirm_password", ""),
                    rx.set_focus("confirm_password"),
                ]
                return
            # Create the new user and add it to the database.
            new_user = UserAccount()  # type: ignore
            new_user.username = username
            new_user.email = email
            new_user.password_hash = UserAccount.hash_password(password)
            # Fetch the city from the database.
            city_str = form_data["city"].split(" ")[0]
            postal_code_str = form_data["city"].split(" ")[1][1:-1]
            city = session.exec(
                City.select().where(
                    City.name == city_str, City.postal_code == postal_code_str
                )
            ).one_or_none()
            new_user.city = city.id
            session.add(new_user)
            session.commit()
        # Set success and redirect to login page after a brief delay.
        self.error_message = ""
        self.success = True
        yield
        await asyncio.sleep(0.5)
        yield [rx.redirect(LOGIN_ROUTE), RegistrationState.set_success(False)]


@rx.page(route=REGISTER_ROUTE, on_load=RegistrationState.load_cities)
def registration_page() -> rx.Component:
    """Render the registration page.

    Returns:
        A reflex component.
    """
    register_form = rx.form(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "Nom d'utilisateur",
                    size="3",
                    weight="medium",
                    text_align="left",
                ),
                rx.input(
                    id="username",
                    size="3",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Email",
                        size="3",
                        weight="medium",
                        text_align="left",
                    ),
                    rx.text(
                        "(visible des autres membres)",
                        size="3",
                        weight="regular",
                        text_align="left",
                        color_scheme="gray",
                    ),
                ),
                rx.input(
                    id="email",
                    # type="email",
                    size="3",
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
                ),
                rx.input(
                    id="password",
                    type="password",
                    size="3",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Confirmation",
                    size="3",
                    weight="medium",
                    text_align="left",
                ),
                rx.input(
                    id="confirm_password",
                    type="password",
                    size="3",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.center(
                rx.divider(size="3"),
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Localisation (ou ville proche)",
                    size="3",
                    weight="medium",
                    text_align="left",
                ),
                rx.select(
                    RegistrationState.cities_as_str,
                    name="city",
                    placeholder="Choisis ta ville",
                    size="3",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.button(
                "Rejoindre",
                type="submit",
                size="3",
                width="100%",
            ),
            rx.center(
                rx.link(
                    rx.text("Déjà un compte ?"),
                    href=LOGIN_ROUTE,
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
        on_submit=RegistrationState.handle_registration,
    )
    return rx.fragment(
        rx.container(
            rx.hstack(
                sidebar(),
                rx.cond(
                    RegistrationState.success,
                    rx.center(
                        rx.vstack(
                            rx.text("Compte créé avec succès."),
                            rx.spinner(),
                            align="center",
                        ),
                        width="100%",
                    ),
                    rx.vstack(
                        register_form,
                        rx.center(
                            rx.cond(  # conditionally show error messages
                                RegistrationState.error_message != "",
                                rx.text(RegistrationState.error_message),
                            ),
                            width="100%",
                        ),
                    ),
                ),
                justify="center",
            )
        )
    )
