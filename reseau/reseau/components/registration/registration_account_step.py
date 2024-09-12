from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from re import match
import reflex as rx

from reseau.components.custom.react_oauth_google import (
    GoogleLogin,
    GoogleOAuthProvider
)
from reseau.models import UserAccount
from reseau.reseau import GOOGLE_AUTH_CLIENT_ID, HOME_ROUTE, LOGIN_ROUTE


def first_name():
    return rx.vstack(
        rx.input(
            id='first_name',
            placeholder='Prénom',
            size='3',
            width='225px',
            on_change=RegistrationAccountStepState.set_first_name,
        ),
        justify='start',
        spacing='1',
    ),


def last_name():
    return rx.vstack(
        rx.input(
            id='last_name',
            placeholder='Nom',
            size='3',
            width='225px',
            on_change=RegistrationAccountStepState.set_last_name,
        ),
        justify='start',
        spacing='1',
    ),


def email():
    return rx.vstack(
        rx.input(
            id='email',
            placeholder='Email',
            size='3',
            width='225px',
            on_change=RegistrationAccountStepState.set_email,
        ),
        justify='start',
        spacing='1',
    ),


def password():
    return rx.vstack(
        rx.input(
            rx.cond(
                RegistrationAccountStepState.password_type ==
                'password',
                rx.icon(
                    'eye',
                    size=20,
                    style=rx.Style(
                        margin_right='0.4em',
                        padding='0.1em',
                        cursor='pointer',
                    ),
                    on_click=RegistrationAccountStepState.toggle_password_type,  # noqa: E501
                ),
                rx.icon(
                    'eye-off',
                    size=20,
                    style=rx.Style(
                        margin_right='0.4em',
                        padding='0.1em',
                        cursor='pointer',
                    ),
                    on_click=RegistrationAccountStepState.toggle_password_type,  # noqa: E501
                ),
            ),
            id='password',
            placeholder='Mot de passe',
            type=RegistrationAccountStepState.password_type,
            size='3',
            width='225px',
            align_items='center',
            on_change=RegistrationAccountStepState.set_password,
        ),
        justify='start',
        spacing='1',
    ),


class RegistrationAccountStepState(rx.State):
    '''
    Handle the account step of registration and
    redirect to profile step.
    '''
    first_name: str = ''
    last_name: str = ''
    email: str = ''

    password: str = ''
    password_type: str = ''

    def init(self):
        '''
        Initialize the state.
        Make sure the password and confirm password fields
        are hidden by default.
        '''
        self.password_type = 'password'

    def toggle_password_type(self):
        '''Toggle password visibility.'''
        self.password_type = (
            'text' if self.password_type == 'password' else 'password'
        )

    async def on_google_auth_success(self, id_token: dict):
        from reseau.pages.registration import RegistrationState

        user_data = None
        try:
            user_data = verify_oauth2_token(
                id_token["credential"],
                requests.Request(),
                GOOGLE_AUTH_CLIENT_ID,
            )
        except Exception:
            yield rx.toast.error("La vérification du compte Google a échoué.")
            return

        # Directly login if the user detected from
        # the google account is already registered
        with rx.session() as session:
            existing_user = (
                session.exec(
                    UserAccount.select()
                    .where(UserAccount.email == user_data['email'])
                ).one_or_none()
            )
        if existing_user is not None:
            registration = await self.get_state(RegistrationState)
            registration._google_login(
                existing_user.id,
                user_data
            )
            yield [
                rx.redirect(HOME_ROUTE),
                RegistrationState.set_account_success(False),
                RegistrationState.set_registration_success(False),
            ]
            return

        registration = await self.get_state(RegistrationState)
        registration.new_user = UserAccount(
            first_name=user_data['given_name'].title(),
            last_name=user_data['family_name'].title(),
            email=user_data['email'],
            enabled=True,
        )
        registration.is_google_auth = True
        registration.google_credentials = user_data
        registration.account_success = True

    async def handle_account(
        self, form_data
    ):
        '''Handle registration form on_submit.
        Args:
            form_data: A dict of form fields and values.
        '''
        from reseau.pages.registration import RegistrationState

        existing_user = None

        first_name = form_data['first_name']
        if not first_name:
            first_name = self.first_name
        if not first_name:
            yield rx.set_focus('first_name')
            yield rx.toast.error("Ton prénom est requis.")
            return

        last_name = form_data['last_name']
        if not last_name:
            last_name = self.last_name
        if not last_name:
            yield rx.set_focus('last_name')
            yield rx.toast.error("Ton nom est requis.")
            return

        email = form_data['email']
        if not email:
            email = self.email
        if not email:
            yield rx.set_focus('email')
            yield rx.toast.error("Ton e-mail est requis.")
            return
        with rx.session() as session:
            existing_user = session.exec(
                UserAccount.select().where(UserAccount.email == email)
            ).one_or_none()
        if existing_user is not None:
            yield rx.set_focus('email')
            yield rx.toast.error(
                "Cet e-mail est déjà utilisé. \
                    Essaie-en un autre."
            )
            return
        # Define a regex pattern for validating the email
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # Use the re package to check if the email matches the pattern
        if not match(pattern, email):
            yield rx.set_focus('email')
            yield rx.toast.error("L'e-mail n'est pas valide.")
            return

        password = form_data['password']
        if not password:
            password = self.password
        if not password:
            yield rx.set_focus('password')
            yield rx.toast.error("Un mot de passe est requis.")
            return
        # Define a regex pattern for validating that the password contains
        # at least one digit, one uppercase letter, one lowercase letter,
        # one special character, and is at least ten characters long.
        pattern = (
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])'
            r'[A-Za-z\d@$!%*?&]{10,}$'
        )
        # Use the re package to check if the password matches the pattern
        if not match(pattern, password):
            yield [
                rx.set_value('password', ''),
                rx.set_focus('password'),
            ]
            yield rx.toast.error(
                "Le mot de passe doit contenir 1 chiffre, \
                    1 lettre majuscule, 1 lettre minuscule, \
                    1 caractère spécial et comporter au moins \
                    10 caractères."
            )
            return

        # Pass user data to registration page
        # and set account step success
        registration = await self.get_state(RegistrationState)
        registration.new_user = UserAccount(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=UserAccount.hash_password(password),
            enabled=True,
        )
        registration.account_success = True


def account_step():
    return rx.form(
        rx.vstack(
            rx.center(
                rx.vstack(
                    rx.text(
                        "Rejoins une communauté de gars ambitieux",
                        font_weight='500',
                        font_size='1.4em',
                        text_align='center',
                    ),
                    align_items='center',
                ),
                margin_bottom='1.5em',
            ),

            rx.box(
                GoogleOAuthProvider.create(
                    GoogleLogin.create(
                        text='continue_with',
                        on_success=RegistrationAccountStepState.on_google_auth_success  # noqa: E501
                    ),
                    client_id=GOOGLE_AUTH_CLIENT_ID,
                ),
            ),

            rx.center(
                rx.hstack(
                    rx.divider(
                        size='3',
                        width='100%',
                    ),
                    rx.text(
                        "ou",
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

            rx.tablet_and_desktop(
                rx.hstack(
                    first_name(),
                    last_name(),
                    justify_content='center',
                ),
            ),
            rx.mobile_only(
                first_name(),
                last_name(),
            ),

            rx.tablet_and_desktop(
                rx.hstack(
                    email(),
                    password(),
                    justify_content='center',
                ),
            ),
            rx.mobile_only(
                email(),
                password(),
            ),

            rx.button(
                "Continuer",
                type='submit',
                size='3',
                margin_top='1em',
                width='225px',
            ),
            rx.center(
                rx.link(
                    rx.text("Déjà un compte ?"),
                    href=LOGIN_ROUTE,
                    width='100%',
                    text_align='center',
                ),
                direction='column',
                spacing='5',
                width='100%',
            ),
            align_items='center',
        ),
        on_submit=RegistrationAccountStepState.handle_account,
        padding_x='3.5em',
        padding_y='3em',
        border='1px solid #E3E4EB',
        border_radius='0.75em',
        box_shadow='0px 3px 4px 1px rgba(0, 0, 0, 0.05)'
    )
