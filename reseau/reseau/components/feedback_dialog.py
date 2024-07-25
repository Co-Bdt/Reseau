from email.mime.text import MIMEText
import reflex as rx
import smtplib

from ..models import UserAccount


class FeedBackDialog(rx.ComponentState):
    message: str = ""
    user: UserAccount = None

    def on_submit(self, form_data: dict):
        self.message = form_data["feedback"]

        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        with open("./mail_files.txt", 'rb') as fp:
            # Create a text/plain message
            msg = MIMEText(fp.read())

        me = self.user.email
        you = "corentin.baudet.dev@gmail.com"

        msg['Subject'] = 'Feedback for Reseau'
        msg['From'] = "corentinb27@gmail.com"
        # msg['To'] = "contact.reseau-devperso@gmail.com"
        msg['To'] = "corentin.baudet.dev@gmail.com"

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('localhost')
        s.sendmail(me, [you], msg.as_string())
        s.quit()

        return rx.toast.success("Merci pour votre feedback.")

    @classmethod
    def get_component(cls, **props):
        # cls.user = props.pop("user")

        return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    rx.icon("message-square-plus"),
                    color_scheme="gray",
                    width="48px",
                    height="48px",
                    # absolute position in the bottom right corner
                    position="absolute",
                    bottom="100px",
                    right="100px",
                    # fully rounded
                    style={"border-radius": "50%"},
                ),
            ),
            rx.dialog.content(
                rx.dialog.title("Feedback"),
                rx.form.root(
                    rx.input(
                        name="feedback",
                        placeholder="Votre message ici...",
                        multiline=True,
                        rows=5,
                        width="100%",
                    ),
                    rx.flex(
                        rx.button("Envoyer"),
                        margin_top="16px",
                        justify="end",
                    ),
                    on_submit=cls.on_submit,
                ),
            ),
        )


feedback_dialog = FeedBackDialog.create
