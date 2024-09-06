from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from re import match
import reflex as rx

from reseau.components.custom.react_oauth_google import (
    GoogleLogin,
    GoogleOAuthProvider
)
from reseau.models import UserAccount
from reseau.reseau import GOOGLE_AUTH_CLIENT_ID, LOGIN_ROUTE


class RegistrationProfileStepState(rx.State):
    '''
    Handle the account step of registration and
    redirect to profile step.
    '''
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    password: str = ''
    confirm_password: str = ''

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

        # TODO: Directly login if the user detected from
        # the google account is already registered
        existing_user = None

        first_name = form_data['first_name']
        if not first_name:
            yield rx.set_focus('first_name')
            yield rx.toast.error("Ton prénom est requis.")
            return
        last_name = form_data['last_name']
        if not last_name:
            yield rx.set_focus('last_name')
            yield rx.toast.error("Ton nom est requis.")
            return

        email = form_data['email']
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
                rx.set_value('confirm_password', ''),
                rx.set_focus('password'),
            ]
            yield rx.toast.error(
                "Le mot de passe doit contenir 1 chiffre, \
                    1 lettre majuscule, 1 lettre minuscule, \
                    1 caractère spécial et comporter au moins \
                    10 caractères."
            )
            return
        if password != form_data['confirm_password']:
            yield [
                rx.set_value('confirm_password', ''),
                rx.set_focus('confirm_password'),
            ]
            yield rx.toast.error("Les mots de passe ne correspondent pas.")
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
            GoogleOAuthProvider.create(
                GoogleLogin.create(
                    on_success=RegistrationProfileStepState.on_google_auth_success  # noqa: E501
                ),
                client_id=GOOGLE_AUTH_CLIENT_ID,
            ),

            rx.center(
                rx.divider(size='3'),
                width='100%',
            ),

            rx.vstack(
                rx.tablet_and_desktop(
                    rx.text(
                        "Prénom",
                        class_name='desktop-text',
                    ),
                ),
                rx.mobile_only(
                    rx.text(
                        "Prénom",
                        class_name='mobile-text',
                    ),
                ),
                rx.input(
                    id='first_name',
                    size='3',
                    on_change=RegistrationProfileStepState.set_first_name,
                    width='100%',
                ),
                justify='start',
                spacing='1',
                width='100%',
            ),
            rx.vstack(
                rx.tablet_and_desktop(
                    rx.text(
                        "Nom",
                        class_name='desktop-text',
                    ),
                ),
                rx.mobile_only(
                    rx.text(
                        "Nom",
                        class_name='mobile-text',
                    ),
                ),
                rx.input(
                    id='last_name',
                    size='3',
                    on_change=RegistrationProfileStepState.set_last_name,
                    width='100%',
                ),
                justify='start',
                spacing='1',
                width='100%',
            ),
            rx.vstack(
                rx.tablet_and_desktop(
                    rx.text(
                        "Email",
                        class_name='desktop-text',
                    ),
                ),
                rx.mobile_only(
                    rx.text(
                        "Email",
                        class_name='mobile-text',
                    ),
                ),
                rx.input(
                    id='email',
                    size='3',
                    on_change=RegistrationProfileStepState.set_email,
                    width='100%',
                ),
                justify='start',
                spacing='1',
                width='100%',
            ),
            rx.vstack(
                rx.tablet_and_desktop(
                    rx.text(
                        "Mot de passe",
                        class_name='desktop-text',
                    ),
                ),
                rx.mobile_only(
                    rx.text(
                        "Mot de passe",
                        class_name='mobile-text',
                    ),
                ),
                rx.input(
                    id='password',
                    type='password',
                    size='3',
                    on_change=RegistrationProfileStepState.set_password,
                    width='100%',
                ),
                justify='start',
                spacing='1',
                width='100%',
            ),
            rx.vstack(
                rx.tablet_and_desktop(
                    rx.text(
                        "Confirmation",
                        class_name='desktop-text',
                    ),
                ),
                rx.mobile_only(
                    rx.text(
                        "Confirmation",
                        class_name='mobile-text',
                    ),
                ),
                rx.input(
                    id='confirm_password',
                    type='password',
                    size='3',
                    on_change=RegistrationProfileStepState.set_confirm_password,  # noqa: E501
                    width='100%',
                ),
                justify='start',
                spacing='1',
                width='100%',
            ),
            rx.button(
                "Continuer",
                type='submit',
                size='3',
                width='100%',
                margin_top='1em',
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
        ),
        on_submit=RegistrationProfileStepState.handle_account,
    )
