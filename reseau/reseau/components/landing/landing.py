from email.mime.text import MIMEText
from re import match
from collections.abc import AsyncGenerator
import reflex as rx
import smtplib


from ...models import UserAccount
from ..profile_picture import profile_picture
from ...reseau import REGISTER_ROUTE
from reseau.components.landing.navbar import navbar
from rxconfig import GMAIL_APP_PASSWORD


class LandingState(rx.State):
    is_email_empty: bool = True

    @staticmethod
    def last_user_card(user: UserAccount, is_first: bool = False):
        return profile_picture(
            style=rx.Style(
                width='3.25em',
                height='3.25em',
                margin_left='-1.25em',
            ),
            profile_picture=user.profile_picture
        )

    def handle_email_change(self, email_value):
        if email_value:
            self.is_email_empty = False
        else:
            self.is_email_empty = True

    async def handle_submit(
        self, form_data: dict
    ) -> AsyncGenerator[
        rx.event.EventSpec | list[rx.event.EventSpec] | None,
        None
    ]:
        email = form_data['email']
        print("email", email)
        if not email:
            yield rx.set_focus('email')
            yield rx.toast.error("Ton e-mail est requis.")
            return

        # Define a regex pattern for validating the email
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # Check if the email is valid
        if not match(pattern, email):
            # Display an error message
            yield rx.set_focus('email')
            yield rx.toast.error("L'e-mail n'est pas au bon format.")
            return

        try:
            await self.send_email(email)
        except Exception:
            yield rx.toast.error(
                "Une erreur s'est produite. Réessaye plus tard."
            )

        yield rx.toast.success("Merci pour ta confiance.")

    async def send_email(
        self, email
    ):
        # Open a plain text file for writing.
        # This will create the file if it doesn't exist
        # and truncate (erase) its content if it does.
        with open(
            f"./mail_list/{email}_to_list.txt",
                'w') as fp:
            fp.write(email)

        # Reopen the file in read mode to read its content
        with open(
            f"./mail_list/{email}_to_list.txt",
                'r') as fp:
            fp.seek(0)  # Move the file pointer
            # to the beginning of the file
            msg = MIMEText(fp.read())

        sender = "contact.reseaudevperso@gmail.com"
        recipient = "contact.reseaudevperso@gmail.com"

        msg['Subject'] = 'Request mail list Reseau'
        msg['From'] = sender
        msg['To'] = recipient

        # Connect to Gmail's SMTP server
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # Upgrade the connection to a secure encrypted SSL/TLS connection
        s.starttls()
        # Log in to the SMTP server using your email and password
        s.login(sender, GMAIL_APP_PASSWORD)
        s.sendmail(sender, [recipient], msg.as_string())
        s.quit()


def landing_page(
    last_users: list[UserAccount]
) -> rx.Component:
    return rx.vstack(
        rx.container(
            navbar(),
            padding='0',
            size='4',
            style=rx.Style(
                width='100%',
            ),
        ),
        rx.vstack(
            rx.vstack(
                rx.text(
                    "Rejoins une communauté",
                    rx.hstack(
                        rx.text(
                            "de gars",
                            trim='start',
                        ),
                        rx.text(
                            " ambitieux",
                            trim='start',
                            white_space="pre",
                            color='#FFC53D',
                        ),
                        spacing='0',
                        justify='center',
                    ),
                    style=rx.Style(
                        margin_x='1em',
                        text_align='center',
                        font_weight="700",
                        font_size=['1.75em', '2.125em', '2.75em', '3.5em'],
                        font_family='Inter, sans-serif',
                    ),
                ),
                spacing='0',
                align='center',
                style=rx.Style(
                    margin_top='5em',
                ),
            ),

            rx.text(
                rx.tablet_and_desktop(
                    "Une plateforme dédiée au développement personnel pour",
                    rx.text("connecter et progresser avec d'autres gars qui partagent tes valeurs."),  # noqa: E501
                ),
                rx.mobile_only(
                    "Une plateforme dédiée au développement personnel pour ",
                    "connecter et progresser avec d'autres gars qui partagent tes valeurs."  # noqa: E501
                ),
                style=rx.Style(
                    margin_x='1em',
                    color='#64748B',
                    text_align='center',
                    font_size=['0.9em', '1em', '1.125em', '1.25em'],
                    font_family='Inter, sans-serif',
                ),
            ),
            rx.link(
                rx.button(
                    "Rejoindre",
                    size='4',
                    style=rx.Style(
                        width='10em',
                        box_shadow='0 4px 4px 0 rgba(0, 0, 0, 0.25)',
                    ),
                ),
                href=REGISTER_ROUTE,
                margin_top='0.5em',
            ),
            spacing='5',
            justify='center',
            align='center',
        ),

        # Display the last 5 useraccount created
        # rx.desktop_only(
        rx.text(
            "Derniers membres inscrits :",
            class_name='desktop-text',
            style=rx.Style(
                margin_top='6em',
                color='#64748B',
                font_size=['0.9em', '1em'],
                font_family='Satoshi Variable, sans-serif',
            )
        ),
        # ),
        # rx.mobile_and_tablet(
        #     rx.text(
        #         "Derniers membres inscrits :",
        #         class_name='discreet-text',
        #     ),
        # ),
        rx.hstack(
            rx.foreach(
                last_users,
                lambda user: LandingState.last_user_card(user),
            ),
            spacing='0',
            style=rx.Style(
                margin_left='1.25em',
                margin_bottom='4em',
            ),
        ),

        # Step by step
        rx.box(
            rx.container(
                rx.vstack(
                    rx.text(
                        "Participe à l'expansion d'une communauté solide",
                        style=rx.Style(
                            color='white',
                            font_weight="600",
                            font_size='1.5em',
                            font_family='Inter, sans-serif',
                        ),
                    ),
                    align='center',
                ),
                size='4',
                padding='0',
            ),
            width='100%',
            background_color='black'
        ),

        rx.form.root(
            rx.vstack(
                rx.desktop_only(
                    rx.text(
                        "Tu préfères être notifié des prochaines mises à "
                        "jours majeures ? "
                        "(pas de spam, promis)",
                        class_name='desktop-text',
                        style={
                            'text_align': 'center',
                        }
                    ),
                ),
                rx.mobile_and_tablet(
                    rx.text(
                        "Tu préfères être notifié des prochaines mises à "
                        "jours majeures ? "
                        "(pas de spam, promis)",
                        class_name='mobile-text',
                        style={
                            'text_align': 'center',
                        }
                    ),
                ),
                rx.hstack(
                    rx.input(
                        id='email',  # for the set_focus event
                        name='email',  # for the form_data
                        placeholder="Ton email",
                        on_change=LandingState.handle_email_change,
                        min_width=['0', '0', '260px'],
                    ),
                    rx.cond(
                        LandingState.is_email_empty,
                        rx.button(
                            "Envoyer",
                            disabled=True
                        ),
                        rx.form.submit(
                            rx.button(
                                "Envoyer",
                                type='submit',
                            ),
                        ),
                    ),
                ),
                direction='column',
                spacing='4',
                align='center',
            ),
            on_submit=LandingState.handle_submit,
            reset_on_submit=True,
            style=rx.Style(
                align='center',
                width='100%',
                background_color=rx.color('gray'),
            ),
        ),
        width='100%',
        align='center',
    )
