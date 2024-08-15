from __future__ import annotations
from collections.abc import AsyncGenerator
from pathlib import Path
from re import match

import asyncio
import boto3
import reflex as rx

from ..common.base_state import BaseState
from ..common.template import template
from .log_in import LOGIN_ROUTE
from ..models import City, UserAccount
from ..reseau import REGISTER_ROUTE
from rxconfig import S3_BUCKET_NAME


class RegistrationState(BaseState):
    '''Handle registration form submission and
    redirect to login page after registration.'''
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    password: str = ''
    confirm_password: str = ''
    city: str = ''

    success: bool = False
    profile_pic: str = ''
    cities_as_str: list[str] = []

    def init(self):
        with rx.session() as session:
            cities = session.exec(
                City.select().order_by(City.name)
            ).all()
        self.cities_as_str = [f'{city.name} ({city.postal_code})'
                              for city in cities]
        self.cities_as_str = sorted(self.cities_as_str)
        # Set the default profile image.
        self.profile_pic = "blank_profile_picture"

    async def handle_upload(self, files: list[rx.UploadFile]):
        '''Handle the upload of file(s).

        Args:
            files: The uploaded file(s).
        '''
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open('wb') as file_object:
                file_object.write(upload_data)

            # Update the profile_img var.
            self.profile_pic = file.filename

    async def handle_registration(
        self, form_data
    ) -> AsyncGenerator[
        rx.event.EventSpec | list[rx.event.EventSpec] | None,
        None
    ]:
        '''Handle registration form on_submit.
        Args:
            form_data: A dict of form fields and values.
        '''
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)
        existing_user = None

        first_name = self.first_name
        if not first_name:
            yield rx.set_focus('first_name')
            yield rx.toast.error("Ton prénom est requis.")
            return
        last_name = self.last_name
        if not last_name:
            yield rx.set_focus('last_name')
            yield rx.toast.error("Ton nom est requis.")
            return

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
        if password != self.confirm_password:
            yield [
                rx.set_value('confirm_password', ''),
                rx.set_focus('confirm_password'),
            ]
            yield rx.toast.error("Les mots de passe ne correspondent pas.")
            return

        city_object = self.city
        if not city_object:
            yield rx.toast.error("La ville ne peut pas être vide.")
            return

        if self.profile_pic == "blank_profile_picture":
            yield rx.toast.error(
                "N'oublie pas d'ajouter une photo de profil."
            )
            return

        new_user = self.complete_registration(
            new_user=UserAccount(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=UserAccount.hash_password(password),
                profile_picture=self.profile_pic,
            ),
            city_object=city_object,
        )

        # Set success and redirect to login page after a brief delay.
        self.success = True
        yield
        await asyncio.sleep(0.5)

        # Create the user's directory
        Path(
            rx.get_upload_dir() /
            f'{new_user.id}'
        ).mkdir(parents=True, exist_ok=True)

        try:
            # Download the profile picto make it readable
            # by the rest of the app.
            bucket.download_file(
                new_user.profile_picture,
                rx.get_upload_dir() / f'{new_user.id}' / f'{self.profile_pic}',
            )
        except Exception:
            pass

        yield [rx.redirect(LOGIN_ROUTE), RegistrationState.set_success(False)]

    def complete_registration(
        self, new_user: UserAccount, city_object
    ) -> UserAccount:
        '''
        Complete the registration process if everything is valid.
        '''

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)

        city_str = city_object.split(' ')[0]
        postal_code_str = city_object.split(' ')[1][1:-1]

        # Add the new user to the database.
        with rx.session() as session:

            # Fetch the city from the database.
            city_object = session.exec(
                City.select().where(
                    City.name == city_str, City.postal_code == postal_code_str
                )
            ).one_or_none()

            new_user.city_id = city_object.id
            session.add(new_user)
            session.commit()

            # To make sure we get the id of the new user,
            # we need to refresh the session.
            session.refresh(new_user)

            # Update the user profile picture with its id as prefix.
            new_user.profile_picture = f'{new_user.id}/{self.profile_pic}'
            session.commit()
            session.refresh(new_user)

            try:
                # Upload the profile picture to S3
                bucket.upload_file(
                    f'{rx.get_upload_dir()}/{self.profile_pic}',
                    f'{new_user.profile_picture}'
                )
            except Exception:
                pass

        return new_user


@rx.page(route=REGISTER_ROUTE, on_load=RegistrationState.init)
@template
def registration_page() -> rx.Component:
    '''Render the registration page.

    Returns:
        A reflex component.
    '''
    registration_form = rx.form(
        rx.vstack(
            rx.hstack(
                rx.upload(
                    rx.image(
                        src=rx.get_upload_url(RegistrationState.profile_pic),
                        width='5em',
                        height='5em',
                        border='1px solid #ccc',
                        border_radius='50%',
                    ),
                    id='profile_img',
                    padding='0px',
                    width='5em',
                    height='5em',
                    border='none',
                    multiple=False,
                    accept={
                        'image/png': ['.png'],
                        'image/jpeg': ['.jpg', '.jpeg'],
                    },
                    on_drop=RegistrationState.handle_upload(
                        rx.upload_files(upload_id='profile_img')
                    ),
                ),
                width='100%',
                justify='center',
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
                    value=RegistrationState.first_name,
                    on_change=RegistrationState.set_first_name,
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
                    value=RegistrationState.last_name,
                    on_change=RegistrationState.set_last_name,
                    width='100%',
                ),
                justify='start',
                spacing='1',
                width='100%',
            ),
            rx.vstack(
                rx.tablet_and_desktop(
                    rx.hstack(
                        rx.text(
                            "Email",
                            class_name='desktop-text',
                        ),
                        rx.text(
                            "(visible des autres membres)",
                            class_name='desktop-text',
                            color_scheme='gray',
                        ),
                    ),
                ),
                rx.mobile_only(
                    rx.hstack(
                        rx.text(
                            "Email",
                            class_name='mobile-text',
                        ),
                        rx.text(
                            "(visible des autres membres)",
                            class_name='mobile-text',
                            color_scheme='gray',
                        ),
                    ),
                ),
                rx.input(
                    id='email',
                    size='3',
                    value=RegistrationState.email,
                    on_change=RegistrationState.set_email,
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
                    value=RegistrationState.password,
                    on_change=RegistrationState.set_password,
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
                    value=RegistrationState.confirm_password,
                    on_change=RegistrationState.set_confirm_password,
                    width='100%',
                ),
                justify='start',
                spacing='1',
                width='100%',
            ),
            rx.center(
                rx.divider(size='3'),
                width='100%',
            ),
            rx.vstack(
                rx.tablet_and_desktop(
                    rx.text(
                        "Localisation (ou ville proche)",
                        class_name='desktop-text',
                    ),
                ),
                rx.mobile_only(
                    rx.text(
                        "Localisation (ou ville proche)",
                        class_name='mobile-text',
                    ),
                ),
                rx.select(
                    RegistrationState.cities_as_str,
                    name='city',
                    placeholder="Choisis ta ville",
                    size='3',
                    value=RegistrationState.city,
                    on_change=RegistrationState.set_city,
                    width='100%',
                ),
                justify='start',
                spacing='1',
                width='100%',
            ),
            rx.button(
                "Rejoindre",
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
            width='100%',
            justify='center',
            min_height='80vh',
        ),
        margin='0',
        on_submit=RegistrationState.handle_registration,
    )

    return rx.cond(
        RegistrationState.is_hydrated,
        rx.box(
            rx.vstack(
                registration_form,
                rx.cond(
                    RegistrationState.success,
                    rx.center(
                        rx.vstack(
                            rx.spinner(),
                            rx.text(
                                "Inscription réussie",
                                size='3',
                                weight='medium',
                            ),
                            align='center',
                        ),
                        width='100%',
                    ),
                    # This is a placeholder for the success message
                    # to always takes the space.
                    rx.vstack(
                        rx.spinner(
                            visibility='hidden',
                        ),
                        rx.text(
                            "Inscription réussie",
                            size='3',
                            weight='medium',
                            visibility='hidden',
                        ),
                    ),
                ),
                position='absolute',
                top='50%',
                left='50%',
                transform='translateX(-50%) translateY(-50%)',
                min_width='260px',
            ),
        ),
    )
