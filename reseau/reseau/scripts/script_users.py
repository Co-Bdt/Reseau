import reflex as rx
from ..models.user_account import UserAccount


def delete_users():
    """Script to delete all users in the database."""

    print("Deleting users in the database")
    with rx.session() as session:
        users = session.exec(UserAccount.select()).all()
        rx.foreach(users, lambda user: session.delete(user))
        # session.delete(users)
        session.commit()

    print("Deleting users - Done")
