from email.mime.text import MIMEText
from re import match
from collections.abc import AsyncGenerator
import reflex as rx
import smtplib

from ..components.profile_picture import profile_picture
from ..models import UserAccount
from ..reseau import REGISTER_ROUTE
from rxconfig import GMAIL_APP_PASSWORD


class LandingState(rx.State):
    is_email_empty: bool = True

    @staticmethod
    def last_user_card(user: UserAccount):
        return rx.card(
            rx.hstack(
                profile_picture(
                    style={
                        'width': '2em',
                        'height': '2em',
                    },
                    profile_picture=user.profile_picture
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            user.first_name,
                            class_name='mobile-text',
                            # Crop the text if too long
                            style={
                                'text_overflow': 'ellipsis',
                                'white_space': 'nowrap',
                                'overflow': 'hidden',
                            }
                        ),
                        rx.text(
                            user.last_name,
                            class_name='mobile-text',
                            style={
                                'text_overflow': 'ellipsis',
                                'white_space': 'nowrap',
                                'overflow': 'hidden',
                            }
                        ),
                        spacing='1',
                    ),
                    rx.text(
                        user.city.name,
                        class_name='discreet-text',
                    ),
                    spacing='0',
                ),
            ),
            width='16em',
            margin_bottom='0.5em',
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
        rx.vstack(
            rx.desktop_only(
                rx.heading(
                    "Reseau",
                    trim='start',
                    style={
                        'font_size': '2.5em',
                        'letter_spacing': '1px',
                    }
                ),
            ),
            rx.mobile_and_tablet(
                rx.heading(
                    "Reseau",
                    trim='start',
                    style={
                        'font_size': '2em',
                        'letter_spacing': '1px',
                        'margin': '0',
                    }
                ),
            ),
            rx.desktop_only(
                rx.text(
                    "La première plateforme pour connecter "
                    "avec des gars en développement personnel",
                    style={
                        'font_size': '1.2em',
                        'text_align': 'center',
                        'margin_bottom': '1em',
                    },
                ),
            ),
            rx.mobile_and_tablet(
                rx.text(
                    "La première plateforme pour connecter\n"
                    "avec des gars en développement personnel",
                    class_name='desktop-text',
                    style={
                        'text_align': 'center',
                        'white_space': 'pre-line',
                    }
                ),
            ),
            rx.link(
                rx.button("Rejoindre", size='3'),
                href=REGISTER_ROUTE,
                is_external=False
            ),
            spacing='5',
            justify='center',
            align='center',
            margin_top='4em',
        ),

        rx.separator(
            margin_top='3em',
            margin_bottom='3em',
        ),

        # Display the last 2 useraccount created
        rx.mobile_and_tablet(
            rx.text(
                "Derniers inscrits :",
                class_name='mobile-text',
                style={
                    'text_align': 'center',
                }
            ),
        ),
        rx.desktop_only(
            rx.text(
                "Derniers inscrits :",
                class_name='desktop-text',
                style={
                    'text_align': 'center',
                }
            ),
        ),
        rx.box(
            rx.foreach(
                last_users,
                lambda user: LandingState.last_user_card(user)
            ),
            margin_bottom='3em',
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
            align='center',
            width='100%',
        ),
        align='center',
    )
