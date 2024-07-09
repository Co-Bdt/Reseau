from passlib.context import CryptContext
from sqlmodel import Field
import reflex as rx

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAccount(
    rx.Model,
    table=True
):
    """A local User model with bcrypt password hashing."""

    username: str = Field(unique=True, nullable=False, index=True)
    email: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)
    city: int = Field(nullable=False)
    profile_text: str = Field(nullable=True)
    enabled: bool = Field(default=True)
    # TODO Add enabled flag to disable accounts instead of deleting them

    @staticmethod
    def hash_password(secret: str) -> str:
        """Hash the secret using bcrypt.

        Args:
            secret: The password to hash.

        Returns:
            The hashed password.
        """
        return pwd_context.hash(secret)

    def verify_password(self, secret: str) -> bool:
        """Validate the user's password.

        Args:
            secret: The password to check.

        Returns:
            True if the hashed secret matches this user's password_hash.
        """
        return pwd_context.verify(
            secret,
            self.password_hash,
        )

    def clean_profile_text(self, profile_text: str) -> str:
        """Clean the profile text for display.

        Args:
            profile_text: The profile text to clean.

        Returns:
            The cleaned profile text.
        """
        return profile_text.replace("\n", " ")
