from email.mime.text import MIMEText
import smtplib

from ..models import Post, UserAccount
from rxconfig import GMAIL_APP_PASSWORD


def post_notification_template(
    user: UserAccount,
    post: Post
):
    """
    Returns a string template for a post notification email.
    """
    return f"""Salut {user.first_name},

Ce post vient d'être publié : "{post.title}".

Jette-y un œil sur https://reseau-devperso.fr,
 et n'hésite pas à laisser un commentaire !

Tu peux à tout moment désactiver ces notifications dans ton profil.

À bientôt gars."""


def pm_notification_template(
    user: UserAccount,
    sender: UserAccount = None
):
    """
    Returns a string template for a private message notification email.
    """
    return f"""Salut {user.first_name},

Tu as reçu un nouveau message de {sender.first_name} {sender.last_name}.

Connecte-toi sur https://reseau-devperso.fr pour le lire et y répondre.

Tu peux à tout moment désactiver ces notifications dans ton profil.

À bientôt gars."""


def write_email_file(
    file_path: str, content: str
) -> MIMEText:
    """
    Write an email to a file.
    Returns:
        A MIMEText object.
    """

    # Open a plain text file for writing.
    # This will create the file if it doesn't exist
    # and truncate (erase) its content if it does.
    with open(file_path, 'w') as fp:
        fp.write(content)

    # Reopen the file in read mode to read its content
    with open(file_path, 'r') as fp:
        fp.seek(0)  # Move the file pointer to the beginning of the file
        message = MIMEText(fp.read())

    return message


def send_email(content: MIMEText, subject: str, recipient: str):
    """
    Send an email using the SMTP protocol.
    """

    sender = 'contact.reseaudevperso@gmail.com'

    content['Subject'] = subject
    content['From'] = sender
    content['To'] = recipient

    try:
        # Connect to Gmail's SMTP server
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # Upgrade the connection to a secure encrypted SSL/TLS connection
        s.starttls()
        # Log in to the SMTP server using your email and password
        s.login(sender, GMAIL_APP_PASSWORD)
        s.sendmail(sender, [recipient], content.as_string())
        s.quit()
    except Exception:
        ...
