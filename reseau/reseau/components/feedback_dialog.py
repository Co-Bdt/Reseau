import reflex as rx

from ..models import UserAccount
from ..common import email


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
    message: str = ''

    def on_submit(self, form_data: dict):
        user = form_data['user'].split('-')

        msg = email.write_email_file(
            f"./feedbacks/{user[0]}_mail_files.txt",
            f"{user[1]} {user[2]}\n{self.message}"
        )

        email.send_email(
            msg,
            'Feedback Reseau',
            'contact.reseaudevperso@gmail.com'
        )

        self.set_message('')
        return rx.toast.success(
            f"Merci {user[1]} pour ton feedback."
        )


def feedback_dialog(
    authenticated_user: UserAccount,
) -> rx.Component:
    '''
    Render a dialog to collect feedback from users.

    Returns:
        A reflex component.
    '''
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon('mic-vocal'),
                **icon_button_style,
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Feedback",
                font_family='Inter, sans-serif',
                font_size='1.4em',
            ),
            rx.flex(
                rx.text(
                    "Qu'est-ce qu'il manque ou pourraît"
                    " être mieux sur la plateforme selon toi ?",
                    font_family='Inter, sans-serif',
                ),
                rx.form.root(
                    rx.input(
                        id='user',
                        value=(
                            f"{authenticated_user.id}-"
                            f"{authenticated_user.first_name}-"
                            f"{authenticated_user.last_name}"
                        ),
                        display='none',
                    ),
                    rx.debounce_input(
                        rx.text_area(
                            name='feedback',
                            placeholder="Ton message ici...",
                            value=FeedbackDialogState.message,
                            on_change=FeedbackDialogState.set_message,
                            multiline=True,
                            rows='5',
                            style=rx.Style(
                                font_family='Inter, sans-serif',
                                width='100%',
                            ),
                        ),
                        debounce_timeout=1000,
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                rx.text(
                                    "Annuler",
                                    font_family='Inter, sans-serif'
                                ),
                                color_scheme='gray',
                                variant='soft',
                            ),
                        ),
                        rx.cond(
                            FeedbackDialogState.message,
                            rx.dialog.close(
                                rx.button(
                                    rx.text(
                                        "Envoyer",
                                        font_family='Inter, sans-serif'
                                    ),
                                    type='submit'
                                ),
                            ),
                            rx.dialog.close(
                                rx.button(
                                    rx.text(
                                        "Envoyer",
                                        font_family='Inter, sans-serif'
                                    ),
                                    type='submit',
                                    disabled=True
                                ),
                            ),
                        ),
                        spacing='3',
                        margin_top='16px',
                        justify='end',
                    ),
                    on_submit=FeedbackDialogState.on_submit,
                ),
                direction='column',
                spacing='4',
            ),
        ),
    )
