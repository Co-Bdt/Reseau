from __future__ import annotations
import asyncio
from collections.abc import AsyncGenerator
from re import match
import reflex as rx

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

    cities_as_str: list[str] = []

    def load_cities(self):
        """Load cities from the database."""
        with rx.session() as session:
            cities = session.exec(
                City.select().order_by(City.name)
            ).all()
        self.cities_as_str = [f"{city.name} ({city.postal_code})"
                              for city in cities]
        self.cities_as_str = sorted(self.cities_as_str)

    async def handle_registration(
        self, form_data
    ) -> AsyncGenerator[rx.event.EventSpec |
                        list[rx.event.EventSpec] | None, None]:
        """Handle registration form on_submit.Merci 
        Args:
            form_data: A dict of form fields and values.
        """
        with rx.session() as session:
            username = form_data["username"]
            if not username:
                yield rx.set_focus("username")
                yield rx.toast.error("Le nom ne peut pas être vide.")
                return
            existing_user = session.exec(
                UserAccount.select().where(UserAccount.username == username)
            ).one_or_none()
            if existing_user is not None:
                yield rx.set_focus("username")
                yield rx.toast.error(
                    f"Le nom d'utilisateur {username} est déjà utilisé. \
                        Essaie-en un autre."
                )
                return
            email = form_data["email"]
            if not email:
                yield rx.set_focus("email")
                yield rx.toast.error("L'email ne peut pas être vide.")
                return
            # Define a regex pattern for validating the email
            pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            # Use the re package to check if the email matches the pattern
            if not match(pattern, email):
                yield rx.set_focus("email")
                yield rx.toast.error("L'email n'est pas valide.")
                return
            password = form_data["password"]
            if not password:
                yield rx.set_focus("password")
                yield rx.toast.error("Le mot de passe ne peut pas être vide.")
                return
            # Define a regex pattern for validating that the password contains
            # at least one digit, one uppercase letter, one lowercase letter,
            # one special character, and is at least ten characters long.
            pattern = (
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])"
                r"[A-Za-z\d@$!%*?&]{10,}$"
            )
            # Use the re package to check if the password matches the pattern
            if not match(pattern, password):
                yield [
                    rx.set_value("password", ""),
                    rx.set_focus("password"),
                ]
                yield rx.toast.error(
                    "Le mot de passe doit contenir un chiffre, \
                        une lettre majuscule, une lettre minuscule, \
                        un caractère spécial et comporter au moins \
                        dix caractères."
                )
                return
            if password != form_data["confirm_password"]:
                yield [
                    rx.set_value("confirm_password", ""),
                    rx.set_focus("confirm_password"),
                ]
                yield rx.toast.error("Les mots de passe ne correspondent pas.")
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
        self.success = True
        yield
        await asyncio.sleep(1)
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
                    width="100%",
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
                    width="100%",
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
            width="100%",
            justify="center",
            min_height="85vh",
        ),
        margin="0",
        on_submit=RegistrationState.handle_registration,
    )
    return rx.fragment(
        rx.vstack(
            rx.container(
                rx.hstack(
                    sidebar(),
                    rx.vstack(
                        register_form,
                        rx.cond(
                            RegistrationState.success,
                            rx.center(
                                rx.vstack(
                                    rx.spinner(),
                                    rx.text(
                                        "Inscription réussie",
                                        size="3",
                                        weight="medium",
                                    ),
                                    align="center",
                                ),
                                width="100%",
                            ),
                        ),
                    ),
                    spacing="0",
                ),
            ),
            align="center",
        ),
    )
