from datetime import datetime
from typing import Optional
from passlib.context import CryptContext
import reflex as rx
from sqlmodel import Column, DateTime, Field, Relationship, func


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAccount(
    rx.Model,
    table=True
):
    """A local UserAccount model with bcrypt password hashing."""

    username: str = Field(unique=True, nullable=False, index=True)
    email: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)
    profile_text: str = Field(nullable=True)
    enabled: bool = Field(default=True)

    # Foreign Keys
    city_id: int = Field(
        nullable=False,
        foreign_key="city.id"
    )

    # Relationships
    auth_session: "AuthSession" = Relationship(
        back_populates="user_account"
    )
    city: "City" = Relationship(
        back_populates="user_account_list"
    )
    interest_list: Optional[list["UserInterest"]] = Relationship(
        back_populates="user"
    )
    post_list: Optional[list["Post"]] = Relationship(
        back_populates="user_account"
    )
    comment_list: Optional[list["Comment"]] = Relationship(
        back_populates="user_account"
    )

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
        if profile_text:
            return profile_text.replace("\n", " ")
        return profile_text
