from __future__ import annotations

import asyncio
import boto3
import reflex as rx

from ..common.base_state import BaseState
from ..common.template import template
from ..components.registration.registration_account_step import RegistrationAccountStepState, account_step  # noqa: E501
from ..components.registration.registration_profile_step import RegistrationProfileStepState, profile_step  # noqa: E501
from ..models import Interest, UserAccount, UserInterest
from ..reseau import HOME_ROUTE, LOGIN_ROUTE, REGISTER_ROUTE
from rxconfig import S3_BUCKET_NAME


class RegistrationState(rx.State):
    '''
    Handle the account step of the registration and
    redirect to the profile step.
    '''
    new_user: UserAccount = None
    is_google_auth: bool = False
    google_credentials: dict = {}

    account_success: bool = False
    registration_success: bool = False

    def init(self):
        self.account_success = False
        self.registration_success = False
        yield RegistrationAccountStepState.init()
        yield RegistrationProfileStepState.init()
        return

    def update_interests(
        self, new_user: UserAccount,
        selected_interests_names: list[str]
    ):
        # Get the corresponding interest objects from the database
        # and store their ids in a list
        selected_interests: list[Interest] = []
        with rx.session() as session:
            selected_interests = session.exec(
                Interest.select()
                .where(Interest.name.in_(selected_interests_names))
            ).all()
        selected_interests_ids = [
            str(interest.id) for interest in selected_interests
        ]

        # Update the new user's interests in the joint table
        with rx.session() as session:
            user_interests = session.exec(
                UserInterest.select().where(
                    UserInterest.useraccount_id == new_user.id
                )
            ).all()
            for user_interest in user_interests:
                session.delete(user_interest)

            for interest_id in selected_interests_ids:
                user_interest = UserInterest(
                    useraccount_id=new_user.id,
                    interest_id=interest_id
                )
                session.add(user_interest)
            session.commit()

    async def complete_registration(
        self,
        selected_interests: list[str],
    ):
        '''
        Complete the user registration process.
        '''

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)

        new_user = self.new_user

        self.registration_success = True
        yield
        await asyncio.sleep(0.5)

        # Add the new user to the database.
        with rx.session() as session:
            session.add(new_user)
            session.commit()

            # To make sure we get the id of the new user,
            # we need to refresh the session.
            session.refresh(new_user)

            # Update the user profile picture with its id as prefix.
            new_user.profile_picture = (
                f'{new_user.id}/' +
                f'{new_user.profile_picture}'
            )
            session.commit()
            session.refresh(new_user)

        try:
            # Upload the profile picture to S3
            bucket.upload_file(
                f'{rx.get_upload_dir()}/' +
                f'{new_user.profile_picture.split("/")[1]}',
                f'{new_user.profile_picture}'
            )
        except Exception:
            pass

        self.update_interests(new_user, selected_interests)

        if self.is_google_auth:
            base_state = await self.get_state(BaseState)
            base_state._google_login(
                new_user.id,
                self.google_credentials
            )
            yield [
                rx.redirect(HOME_ROUTE),
                RegistrationState.set_account_success(False),
                RegistrationState.set_registration_success(False),
            ]
        else:
            yield [
                rx.redirect(LOGIN_ROUTE),
                RegistrationState.set_account_success(False),
                RegistrationState.set_registration_success(False)
            ]


@rx.page(route=REGISTER_ROUTE, on_load=RegistrationState.init)
@template
def registration_page() -> rx.Component:
    '''Render the registration page.

    Returns:
        A reflex component.
    '''

    return rx.cond(
        RegistrationState.is_hydrated,
        rx.vstack(
            rx.cond(
                ~RegistrationState.account_success,
                account_step(),
                profile_step(),
            ),
            rx.cond(
                RegistrationState.registration_success,
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
            align='center',
            justify='center',
            style=rx.Style(
                height='100vh',
                margin='1.25em',
            ),
        ),
    )
