
import reflex as rx

from reseau.components.interest_badges import interest_badges

from ...models import City, Interest


class RegistrationProfileStepState(rx.State):
    '''
    Handle the profile step of the registration and
    redirect to login page.
    '''
    cities_as_str: list[str] = []
    interests_as_str: list[str] = []

    city: str = ''
    profile_pic: str = ''
    # the user's selected interests names
    selected_interests: list[str] = []

    def init(self):
        '''
        Initialize the state.
        '''
        # Set the default profile image.
        self.profile_pic = "blank_profile_picture"

        # Load cities from database
        with rx.session() as session:
            cities = session.exec(
                City.select().order_by(City.name)
            ).all()
        self.cities_as_str = [f'{city.name} ({city.postal_code})'
                              for city in cities]
        self.cities_as_str = sorted(self.cities_as_str)

        # Load interests from database
        with rx.session() as session:
            interests = session.exec(
                Interest.select().order_by(Interest.name)
            ).all()
        self.interests_as_str = [interest.name for interest in interests]

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

    def add_selected_interest(self, item: str):
        # limit selected items to 4
        if len(self.selected_interests) < 4:
            self.selected_interests.append(item)
        else:
            return rx.toast.warning("Tu ne peux sélectionner que 4 intérêts.")

    def remove_selected_interest(self, item: str):
        self.selected_interests.remove(item)

    async def handle_registration(self, form_data):
        '''Handle the registration form submission.

        Args:
            form_data: A dict of form fields and values.
        '''
        from reseau.pages.registration import RegistrationState

        city_object = form_data['city']
        if not city_object:
            yield rx.toast.error("La ville ne peut pas être vide.")
            return

        if len(self.selected_interests) < 2:
            yield rx.toast.error(
                "Tu dois sélectionner au moins deux intérêts."
            )
            return

        if self.profile_pic == "blank_profile_picture":
            yield rx.toast.error(
                "N'oublie pas d'ajouter une photo de profil."
            )
            return

        # Get RegistrationState to use its attributes
        registration = await self.get_state(RegistrationState)

        city_str = city_object.split(' ')[0]
        postal_code_str = city_object.split(' ')[1][1:-1]

        # Fetch the city from the database.
        with rx.session() as session:
            city_object = session.exec(
                City.select().where(
                    City.name == city_str, City.postal_code == postal_code_str
                )
            ).one_or_none()
        registration.new_user.city_id = city_object.id
        registration.new_user.profile_picture = self.profile_pic

        # Pass user selected interests and complete user registration
        # We need to register the user before update its interests
        yield RegistrationState.complete_registration(self.selected_interests)


def profile_step():
    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.upload(
                    rx.image(
                        src=rx.get_upload_url(RegistrationProfileStepState.profile_pic),  # noqa: E501
                        width='5em',
                        height='5em',
                        border_radius='50%',
                        object_fit="cover",
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
                    on_drop=RegistrationProfileStepState.handle_upload(
                        rx.upload_files(upload_id='profile_img')
                    ),
                ),
                width='100%',
                justify='center',
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
                    RegistrationProfileStepState.cities_as_str,
                    name='city',
                    placeholder="Choisis ta ville",
                    size='3',
                    on_change=RegistrationProfileStepState.set_city,
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

            interest_badges(
                interests_names=RegistrationProfileStepState.interests_as_str,
                selected_interests_names=RegistrationProfileStepState.selected_interests,  # noqa: E501
                add_selected=RegistrationProfileStepState.add_selected_interest,  # noqa: E501
                remove_selected=RegistrationProfileStepState.remove_selected_interest,  # noqa: E501
            ),

            rx.button(
                "Rejoindre",
                type='submit',
                size='3',
                width='100%',
                margin_top='1em',
            ),
        ),
        on_submit=RegistrationProfileStepState.handle_registration,
    )
