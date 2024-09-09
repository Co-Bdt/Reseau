from email.mime.text import MIMEText
import reflex as rx
import smtplib

from ..models import UserAccount
from rxconfig import GMAIL_APP_PASSWORD


icon_button_style = {
    'variant': 'surface',
    'width': '48px',
    'height': '48px',
    # absolute position in the bottom right corner
    'position': 'fixed',
    'bottom': ['2em', '2em', '2em', '2em', '100px'],
    'right': ['2em', '2em', '2em', '2em', '100px'],
    # fully rounded
    'border_radius': '50%',
}


class FeedbackDialogState(rx.State):
    message: str = ""

    def on_submit(self, form_data: dict):
        user = form_data['user'].split('-')

        # Open a plain text file for writing.
        # This will create the file if it doesn't exist
        # and truncate (erase) its content if it does.
        with open(
            f"./feedbacks/{user[0]}_mail_files.txt",
                'w') as fp:
            fp.write(f"{user[1]} "
                     f"{user[2]}\n"
                     f"{self.message}")

        # Reopen the file in read mode to read its content
        with open(
            f"./feedbacks/{user[0]}_mail_files.txt",
                'r') as fp:
            fp.seek(0)  # Move the file pointer to the beginning of the file
            msg = MIMEText(fp.read())

        sender = "contact.reseaudevperso@gmail.com"
        recipient = "contact.reseaudevperso@gmail.com"

        msg['Subject'] = 'Feedback Reseau'
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

        self.set_message("")
        return rx.toast.success(f"Merci {user[1]}\
                                 pour ton feedback.")


def feedback_dialog(
    authenticated_user: UserAccount,
) -> rx.Component:
    """
    Render a dialog to collect feedback from users.

    Returns:
        A reflex component.
    """
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("mic-vocal"),
                **icon_button_style,
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Feedback"),
            rx.flex(
                rx.text("Qu'est-ce qu'il manque ou pourraît"
                        " être mieux sur la plateforme selon toi ?"),
                rx.form.root(
                    rx.input(
                        id="user",
                        value=(
                            f"{authenticated_user.id}-"
                            f"{authenticated_user.first_name}-"
                            f"{authenticated_user.last_name}"
                        ),
                        display="none",
                    ),
                    rx.debounce_input(
                        rx.text_area(
                            name="feedback",
                            placeholder="Ton message ici...",
                            value=FeedbackDialogState.message,
                            on_change=FeedbackDialogState.set_message,
                            multiline=True,
                            rows="5",
                            width="100%",
                        ),
                        debounce_timeout=1000,
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Annuler",
                                color_scheme="gray",
                                variant="soft",
                            ),
                        ),
                        rx.cond(
                            FeedbackDialogState.message,
                            rx.dialog.close(
                                rx.button(
                                    "Envoyer",
                                    type="submit"
                                ),
                            ),
                            rx.dialog.close(
                                rx.button(
                                    "Envoyer",
                                    type="submit",
                                    disabled=True
                                ),
                            ),
                        ),
                        spacing="3",
                        margin_top="16px",
                        justify="end",
                    ),
                    on_submit=FeedbackDialogState.on_submit,
                ),
                direction="column",
                spacing="4",
            ),
        ),
    )
