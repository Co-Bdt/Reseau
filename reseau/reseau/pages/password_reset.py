from datetime import datetime, timedelta
from passlib.context import CryptContext
import pytz
from re import match
import reflex as rx
from secrets import token_urlsafe

from ..common import email
from ..models import PasswordReset, UserAccount
from ..reseau import LOGIN_ROUTE, PASSWORD_RESET_ROUTE

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordResetState(rx.State):
    email: str = ''
    new_password: str = ''
    password_type: str = ''
    confirm_new_password: str = ''
    confirm_password_type: str = ''

    def init(self):
        '''
        Initialize the state.
        Make sure the password and confirm password fields
        are hidden by default.
        '''
        self.password_type = 'password'
        self.confirm_password_type = 'password'

    def toggle_password_type(self):
        '''Toggle password visibility.'''
        self.password_type = (
            'text' if self.password_type == 'password' else 'password'
        )

    def toggle_confirm_password_type(self):
        '''Toggle confirm password visibility.'''
        self.confirm_password_type = (
            'text' if self.confirm_password_type == 'password' else 'password'
        )

    def is_password_reset_valid(self, user: UserAccount) -> bool:
        '''
        Check :
        - if the user has been created with a google account
        - if there are others password reset issued for this user
        in the last 24 hours.
        Returns:
            True if the password reset is valid, False otherwise.
        '''
        if user.is_google_account:
            return False

        with rx.session() as session:
            password_resets = session.exec(
                PasswordReset.select()
                .where(PasswordReset.useraccount_id == user.id)
            ).all()
        for pwd_reset in password_resets:
            if (
                pwd_reset.created_at + timedelta(days=1)
                > datetime.now(tz=pytz.UTC)
            ):
                return False
        return True

    def send_reset_email(self, form_data) -> rx.event.EventSpec:
        '''
        Send a password reset email
        if the email is valid
        '''
        user_email = form_data['email']
        if not user_email:
            user_email = self.email

        with rx.session() as session:
            user = session.exec(
                UserAccount.select().where(
                    UserAccount.email == user_email
                )
            ).first()
        if not user or not self.is_password_reset_valid(user):
            return rx.toast.success(
                "Un email de réinitialisation de mot de passe a été envoyé."
            )

        # Generate a token
        token = token_urlsafe(20)

        # Save the token
        password_reset = PasswordReset(
            hash_token=UserAccount.hash_secret(token),
            created_at=datetime.now(tz=pytz.UTC),
            useraccount_id=user.id,
        )
        with rx.session() as session:
            session.add(password_reset)
            session.commit()

        msg = email.write_email_file(
            f"./other_mails/{user.id}_mail_file.txt",
            email.password_reset_template(user, token)
        )
        email.send_email(
            msg,
            'Réinitialisation de mot de passe - Reseau',
            user.email
        )
        return rx.toast.success(
            "Un email de réinitialisation de mot de passe a été envoyé."
        )

    def change_password(self, form_data) -> rx.event.EventSpec:
        '''
        Change the user's password if the token is valid,
        and the new password is valid.
        '''
        token = self.router.page.raw_path.split('/')[2]
        user = None
        with rx.session() as session:
            password_resets = session.exec(
                PasswordReset.select()
            ).all()
            for password_reset in password_resets:
                if pwd_context.verify(
                    token, password_reset.hash_token
                ):
                    user = session.exec(
                        UserAccount.select()
                        .where(UserAccount.id == password_reset.useraccount_id)
                    ).first()
                    break
            if (
                not user or
                password_reset.is_reset
            ):
                return rx.toast.error("Demande de réinitialisation invalide.")

        if password_reset.created_at < (
            datetime.now(tz=pytz.UTC) - timedelta(hours=3)
        ):
            return rx.toast.error("Demande de réinitialisation expirée.")

        new_password = form_data['new_password']
        if not new_password:
            new_password = self.new_password
        confirm_new_password = form_data['confirm_new_password']
        if not confirm_new_password:
            confirm_new_password = self.confirm_new_password

        if not new_password or not confirm_new_password:
            return rx.toast.error("Les champs sont requis")
        # Define a regex pattern for validating that the password contains
        # at least one digit, one uppercase letter, one lowercase letter,
        # one special character, and is at least ten characters long.
        pattern = (
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])'
            r'[A-Za-z\d@$!%*?&]{10,}$'
        )
        # Use the re package to check if the password matches the pattern
        if not match(pattern, new_password):
            return rx.toast.error(
                "Le mot de passe doit contenir au moins 1 chiffre, \
                    1 lettre majuscule, 1 lettre minuscule, \
                    1 caractère spécial et comporter au moins \
                    10 caractères."
            )
        if new_password != confirm_new_password:
            return rx.toast.error("Les mots de passe ne correspondent pas.")
        if user.verify_password(new_password):
            return rx.toast.error(
                "Le nouveau mot de passe doit être différent."
            )

        with rx.session() as session:
            user: UserAccount = session.exec(
                UserAccount.select()
                .where(UserAccount.id == password_reset.useraccount_id)
            ).first()
            user.password_hash = UserAccount.hash_secret(new_password)
            session.add(user)
            session.commit()

            password_reset.is_reset = True
            session.add(password_reset)
            session.commit()
        return rx.redirect(LOGIN_ROUTE)


@rx.page(
    f"{PASSWORD_RESET_ROUTE}/[[...token]]",
    on_load=PasswordResetState.init
)
def password_reset():
    '''
    Page for resetting a user's password.

    Returns:
        A reflex component.
    '''
    def send_email_step():
        return rx.form(
            rx.vstack(
                rx.text(
                    "Saisis l'adresse email associée à ton compte pour "
                    "recevoir un lien de réinitialisation."
                ),
                rx.input(
                    name='email',
                    type='email',
                    placeholder="Adresse email",
                    size='3',
                    width='100%',
                    value=PasswordResetState.email,
                    on_change=PasswordResetState.set_email,
                ),
                rx.button(
                    "Recevoir le lien de réinitialisation",
                    type='submit',
                    size='3',
                    width='100%',
                    margin_top='1em',
                ),
            ),
            on_submit=PasswordResetState.send_reset_email,
            reset_on_submit=True,
        )

    def change_password_step():
        return rx.form(
            rx.vstack(
                rx.input(
                    rx.cond(
                        PasswordResetState.password_type ==
                        'password',
                        rx.icon(
                            'eye',
                            size=20,
                            style=rx.Style(
                                margin_right='0.4em',
                                padding='0.1em',
                                cursor='pointer',
                            ),
                            on_click=PasswordResetState.toggle_password_type,
                        ),
                        rx.icon(
                            'eye-off',
                            size=20,
                            style=rx.Style(
                                margin_right='0.4em',
                                padding='0.1em',
                                cursor='pointer',
                            ),
                            on_click=PasswordResetState.toggle_password_type,
                        ),
                    ),
                    name='new_password',
                    placeholder="Nouveau mot de passe",
                    type=PasswordResetState.password_type,
                    size='3',
                    value=PasswordResetState.new_password,
                    on_change=PasswordResetState.set_new_password,
                    style=rx.Style(
                        width='100%',
                        align_items='center',
                    ),
                ),
                rx.input(
                    rx.cond(
                        PasswordResetState.confirm_password_type ==
                        'password',
                        rx.icon(
                            'eye',
                            size=20,
                            style=rx.Style(
                                margin_right='0.4em',
                                padding='0.1em',
                                cursor='pointer',
                            ),
                            on_click=PasswordResetState.toggle_confirm_password_type,  # noqa: E501
                        ),
                        rx.icon(
                            'eye-off',
                            size=20,
                            style=rx.Style(
                                margin_right='0.4em',
                                padding='0.1em',
                                cursor='pointer',
                            ),
                            on_click=PasswordResetState.toggle_confirm_password_type,  # noqa: E501
                        ),
                    ),
                    name='confirm_new_password',
                    placeholder="Confirmer le nouveau mot de passe",
                    type=PasswordResetState.confirm_password_type,
                    size='3',
                    value=PasswordResetState.confirm_new_password,
                    on_change=PasswordResetState.set_confirm_new_password,
                    style=rx.Style(
                        width='100%',
                        align_items='center',
                    ),
                ),
                rx.button(
                    "Changer le mot de passe",
                    type='submit',
                    size='3',
                    width='100%',
                    margin_top='1em',
                ),
            ),
            on_submit=PasswordResetState.change_password,
            reset_on_submit=True,
        )

    return rx.cond(
        PasswordResetState.is_hydrated,
        rx.vstack(
            rx.text(
                "Mot de passe oublié ?",
                font_weight='700',
                font_size='1.75em',
                style=rx.Style(
                    margin_bottom='0.75em',
                ),
            ),

            rx.cond(
                rx.State.token,
                change_password_step(),
                send_email_step(),
            ),

            style=rx.Style(
                position='absolute',
                top='50%',
                left='50%',
                transform='translateX(-50%) translateY(-50%)',
                width='450px',
                padding_x='3.5em',
                padding_y='3em',
                border='1px solid #E3E4EB',
                border_radius='0.75em',
                box_shadow='0px 3px 4px 1px rgba(0, 0, 0, 0.05)',
            ),
        ),
    )
