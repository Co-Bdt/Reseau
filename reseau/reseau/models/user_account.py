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


class City(
    rx.Model,
    table=True,
):
    """A local City model."""

    name: str = Field(nullable=False)
    postal_code: str = Field(nullable=False)

    # Relationships
    user_account_list: list["UserAccount"] = Relationship(
        back_populates="city"
    )


class Post(
    rx.Model,
    table=True
):
    """A Post model."""

    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published_at: datetime = Field(nullable=False)
    published: bool = True

    # Foreign Keys
    author_id: int = Field(
        nullable=False,
        foreign_key="useraccount.id"
    )

    # Relationships
    user_account: "UserAccount" = Relationship(
        back_populates="post_list"
    )
    comment_list: Optional[list["Comment"]] = Relationship(
        back_populates="post"
    )

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format a datetime for display."""
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class Comment(
    rx.Model,
    table=True
):
    """A Comment model."""

    content: str = Field(nullable=False)
    published_at: datetime = Field(nullable=False)
    published: bool = True

    # Foreign keys
    post_id: int = Field(nullable=False, foreign_key="post.id")
    author_id: int = Field(nullable=False, foreign_key="useraccount.id")

    # Relationships
    post: "Post" = Relationship(
        back_populates="comment_list"
    )
    user_account: "UserAccount" = Relationship(
        back_populates="comment_list"
    )

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format a datetime for display."""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    

class Interest(
    rx.Model,
    table=True
):
    """An Interest model."""

    name: str = Field(nullable=False)

    # Relationships
    user_list: Optional[list["UserInterest"]] = Relationship(
        back_populates="interest"
    )


class UserInterest(
    rx.Model,
    table=True
):
    """A model to join User and his Interest(s)."""

    # Foreign keys
    user_id: int = Field(nullable=False, foreign_key="useraccount.id")
    interest_id: int = Field(nullable=False, foreign_key="interest.id")

    # Relationships
    user: "UserAccount" = Relationship(
        back_populates="interest_list"
    )
    interest: "Interest" = Relationship(
        back_populates="user_list"
    )


class AuthSession(
    rx.Model,
    table=True,
):
    """Correlate a session_id with an arbitrary user_id."""

    user_id: int = Field(
        index=True,
        nullable=False,
        foreign_key="useraccount.id"
    )
    session_id: str = Field(unique=True, index=True, nullable=False)
    expiration: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
    )

    # Relationships
    user_account: "UserAccount" = Relationship(
        back_populates="auth_session",
    )
