from datetime import datetime, timedelta
from passlib.context import CryptContext
import pytz
from re import match
import reflex as rx
from secrets import token_urlsafe

from ..common import email
from ..models import PasswordReset, UserAccount
from ..reseau import PASSWORD_RESET_ROUTE

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordResetState(rx.State):
    email: str = ''
    new_password: str = ''
    confirm_new_password: str = ''

    def is_password_reset_valid(self, user: UserAccount) -> bool:
        '''
        Check if there are others password reset issued for this user
        in the last 24 hours.
        Returns:
            True if the password reset is valid, False otherwise.
        '''
        with rx.session() as session:
            password_resets = session.exec(
                PasswordReset.select()
                .where(PasswordReset.useraccount_id == user.id)
            ).all()
        # TODO: test and remove comments before going preprod
        # for pwd_reset in password_resets:
        #     if (
        #         pwd_reset.created_at + timedelta(days=1)
        #         > datetime.now(tz=pytz.UTC)
        #     ):
        #         return False
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

    def reset_password(self, form_data) -> rx.event.EventSpec:
        '''
        Reset the user's password if the token is valid,
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

            # if password_reset:
            #     user = session.exec(
            #         UserAccount.select()
            #         .where(UserAccount.id == password_reset.useraccount_id)
            #     ).first()
            if (
                not user or
                password_reset.is_reset
            ):
                return rx.toast.error("Demande de réinitialisation invalide.")

        # TODO: test and remove comments before going preprod
        # print("datetime.now()", datetime.now())
        # if password_reset.created_at < (
        #     datetime.now(tz=pytz.UTC) - timedelta(hours=3)
        # ):
        #     return rx.toast.error("Demande de réinitialisation expirée.")

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

        print("new hash:", UserAccount.hash_secret(new_password))
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
        return rx.toast.success("Mot de passe réinitialisé avec succès.")


@rx.page(f"{PASSWORD_RESET_ROUTE}/[[...token]]", 'password_reset')
def password_reset():
    '''
    Page for resetting a user's password.

    Returns:
        A reflex component.
    '''
    return rx.cond(
        PasswordResetState.is_hydrated,
        rx.cond(
            rx.State.token,
            rx.form(
                rx.vstack(
                    # rx.input(
                    #     name='token',
                    #     type='hidden',
                    #     value=rx.State.token,
                    # ),
                    rx.input(
                        name='new_password',
                        placeholder='Nouveau mot de passe',
                        type='password',
                        value=PasswordResetState.new_password,
                        on_change=PasswordResetState.set_new_password,
                    ),
                    rx.input(
                        name='confirm_new_password',
                        placeholder='Confirmer le nouveau mot de passe',
                        type='password',
                        value=PasswordResetState.confirm_new_password,
                        on_change=PasswordResetState.set_confirm_new_password,
                    ),
                    rx.button(
                        'Réinitialiser le mot de passe',
                        type='submit',
                    ),
                ),
                on_submit=PasswordResetState.reset_password,
                reset_on_submit=True,
            ),
            rx.vstack(
                rx.text(
                    "Saisis l'adresse email associée à ton compte pour "
                    "recevoir un lien de réinitialisation de mot de passe."
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            name='email',
                            type='email',
                            placeholder='Adresse email',
                            value=PasswordResetState.email,
                            on_change=PasswordResetState.set_email,
                        ),
                        rx.button(
                            "Réinitialiser le mot de passe",
                            type='submit',
                        ),
                    ),
                    on_submit=PasswordResetState.send_reset_email,
                    reset_on_submit=True,
                ),
            ),
        ),
    )
