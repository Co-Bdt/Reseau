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
                    rx.text(
                        "Rejoindre",
                        style=rx.Style(
                            font_weight="600",
                            font_family='Inter, sans-serif',
                        ),
                    ),
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
                    rx.hstack(
                        rx.text(
                            "Participe à l'expansion d'une communauté",
                            style=rx.Style(
                                color='white',
                                font_weight="700",
                                font_size='2em',
                                font_family='Inter, sans-serif',
                            ),
                        ),
                        rx.text(
                            " soudée",
                            white_space="pre",
                            style=rx.Style(
                                color='#FFC53D',
                                font_weight="700",
                                font_size='2em',
                                font_family='Inter, sans-serif',
                            ),
                        ),
                        spacing='0',
                    ),
                    rx.hstack(
                        rx.image(
                            src="/image_etape1.png",
                            style=rx.Style(
                                radius='0.75em',
                            ),
                        ),
                        rx.vstack(
                            rx.text(
                                "Étape 1",
                                style=rx.Style(
                                    color='#FFC53D',
                                    font_weight="700",
                                    font_size='0.75em',
                                    font_family='Inter, sans-serif',
                                ),
                            ),
                            rx.text(
                                "Crée ton compte",
                                style=rx.Style(
                                    color='white',
                                    font_weight="700",
                                    font_size='1.75em',
                                    font_family='Inter, sans-serif',
                                ),
                            ),
                            rx.text(
                                rx.hstack(
                                    rx.icon('circle-check'),
                                    "Indique ta localisation",
                                ),
                                rx.hstack(
                                    rx.icon('circle-check'),
                                    "Affiche tes intérêts",
                                    style=rx.Style(
                                        margin_top='0.5em',
                                    ),
                                ),
                                style=rx.Style(
                                    margin_top='0.5em',
                                    color='white',
                                    font_family='Satoshi Variable, sans-serif',
                                ),
                            ),
                            spacing='0',
                        ),
                        spacing='9',
                        style=rx.Style(
                            margin_top='5em',
                        ),
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                "Étape 2",
                                style=rx.Style(
                                    color='#FFC53D',
                                    font_weight="700",
                                    font_size='0.75em',
                                    font_family='Inter, sans-serif',
                                ),
                            ),
                            rx.text(
                                "Présente toi",
                                style=rx.Style(
                                    color='white',
                                    font_weight="700",
                                    font_size='1.75em',
                                    font_family='Inter, sans-serif',
                                ),
                            ),
                            rx.text(
                                "Partage ton histoire, tes ambitions",
                                rx.text("et discute avec d'autres gars."),
                                style=rx.Style(
                                    margin_top='0.5em',
                                    color='white',
                                    font_family='Satoshi Variable, sans-serif',
                                ),
                            ),
                            spacing='0',
                        ),
                        rx.image(
                            src="/image_etape2.png",
                            style=rx.Style(
                                radius='0.75em',
                            ),
                        ),
                        spacing='9',
                        style=rx.Style(
                            margin_top='5em',
                        ),
                    ),
                    align='center',
                ),
                size='4',
                padding='0',
            ),
            style=rx.Style(
                width='100%',
                background_color='#020200',
                padding_y='4em',
            ),
        ),

        # Last call to action
        rx.container(
            rx.vstack(
                rx.text(
                    "Prêt à faire des rencontres inestimables ?",
                    style=rx.Style(
                        font_weight="700",
                        font_size='2em',
                        font_family='Inter, sans-serif',
                    ),
                ),
                rx.text(
                    "Reseau est née de l'isolement que ressentent de nombreux",
                    " gars dans leur quête de développement personnel. ",
                    "L'idée est de faire grandir une communauté de personnes ",
                    "qui partagent la même ambition : devenir la meilleure ",
                    "version d'eux-mêmes. Au travers de cette plateforme, ",
                    "tu pourras discuter, partager tes pensées et progresser ",
                    "avec d'autres gars qui partagent tes valeurs. ",
                    "Ce projet est en constante évolution, et nous ",
                    "avons besoin de tes retours pour l'enmener plus loin. ",
                    style=rx.Style(
                        margin_top='1em',
                        font_family='Satoshi Variable, sans-serif',
                    ),
                ),
                rx.link(
                    rx.button(
                        rx.text(
                            "Rejoindre",
                            style=rx.Style(
                                font_weight="600",
                                font_family='Inter, sans-serif',
                            ),
                        ),
                        size='3',
                        style=rx.Style(
                            width='10em',
                            box_shadow='0 4px 4px 0 rgba(0, 0, 0, 0.25)',
                        ),
                    ),
                    href=REGISTER_ROUTE,
                    margin_top='1em',
                ),
                align='center',
                # style=rx.Style(
                #     width='100%',
                #     padding_y='4em',
                # ),
            ),
            size='4',
            padding='4em 0 4em 0',
        ),

        rx.container(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "Des questions ?",
                        style=rx.Style(
                            color='white',
                            font_size='1.25em',
                            font_family='Inter, sans-serif',
                        ),
                    ),
                    rx.link(
                        rx.button(
                            rx.text(
                                "Contacte-nous",
                                style=rx.Style(
                                    font_family='Inter, sans-serif',
                                ),
                            ),
                            size='2',
                            color_scheme='gray',
                        ),
                        href="mailto:contact-reseaudevperso@gmail.com",
                    ),
                    width='20%',
                ),
                rx.form.root(
                    rx.vstack(
                        rx.text(
                            "Tu souhaites être notifié des prochaines mises à "
                            "jours majeures ?",
                            rx.text("(pas de spam, promis)"),
                            style=rx.Style(
                                color='white',
                                font_size='0.9em',
                                font_family='Inter, sans-serif',
                            ),
                        ),
                        rx.hstack(
                            rx.input(
                                id='email',  # for the set_focus event
                                name='email',  # for the form_data
                                placeholder="Ton email",
                                on_change=LandingState.handle_email_change,
                            ),
                            rx.cond(
                                LandingState.is_email_empty,
                                rx.button(
                                    rx.text(
                                        "Envoyer",
                                        style=rx.Style(
                                            font_family='Inter, sans-serif',
                                        ),
                                    ),
                                    disabled=True,
                                    style=rx.Style(
                                        background_color='gray',
                                    ),
                                ),
                                rx.form.submit(
                                    rx.button(
                                        rx.text(
                                            "Envoyer",
                                            style=rx.Style(
                                                font_family='Inter, sans-serif',  # noqa: E501
                                            ),
                                        ),
                                        type='submit',
                                    ),
                                ),
                            ),
                        ),
                        direction='column',
                        spacing='4',
                    ),
                    on_submit=LandingState.handle_submit,
                    reset_on_submit=True,
                ),
                spacing='9',
                align_items='start',
            ),
            size='4',
            padding='4em 0 4em 0',
            style=rx.Style(
                width='100%',
                background_color='#020200',
            ),
        ),
        width='100%',
        align='center',
    )
