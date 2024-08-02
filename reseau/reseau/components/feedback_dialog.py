from email.mime.text import MIMEText
import reflex as rx
import smtplib

from ..common.base_state import BaseState
from rxconfig import GMAIL_APP_PASSWORD


class FeedbackDialogState(BaseState):
    message: str = ""

    def on_submit(self, form_data: dict):
        # Open a plain text file for writing.
        # This will create the file if it doesn't exist
        # and truncate (erase) its content if it does.
        with open(
            f"./feedbacks/{self.authenticated_user.id}_mail_files.txt",
                'w') as fp:
            fp.write(self.message)

        # Reopen the file in read mode to read its content
        with open(
            f"./feedbacks/{self.authenticated_user.id}_mail_files.txt",
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
        return rx.toast.success(f"Merci {self.authenticated_user.username}\
                                 pour ton feedback.")


def feedback_dialog() -> rx.Component:
    """
    Render a dialog to collect feedback from users.

    Returns:
        A reflex component.
    """
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("message-square-quote"),
                color_scheme="gray",
                width="48px",
                height="48px",
                # absolute position in the bottom right corner
                position="fixed",
                bottom="100px",
                right="100px",
                # fully rounded
                style={"border-radius": "50%"},
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Feedback"),
            rx.flex(
                rx.text("Qu'est-ce qui manque ou qui pourraît"
                        " être mieux sur la plateforme pour toi ?"),
                rx.form.root(
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
