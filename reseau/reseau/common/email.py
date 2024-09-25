from email.mime.text import MIMEText
import smtplib

from rxconfig import GMAIL_APP_PASSWORD


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


def send_email(message: MIMEText, subject: str, recipient: str):
    """
    Send an email using the SMTP protocol.
    """

    sender = 'contact.reseaudevperso@gmail.com'

    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    # Connect to Gmail's SMTP server
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # Upgrade the connection to a secure encrypted SSL/TLS connection
    s.starttls()
    # Log in to the SMTP server using your email and password
    s.login(sender, GMAIL_APP_PASSWORD)
    s.sendmail(sender, [recipient], message.as_string())
    s.quit()
