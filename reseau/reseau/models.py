from datetime import datetime
from typing import Optional
from passlib.context import CryptContext
import reflex as rx
from sqlalchemy import ForeignKey, Integer
from sqlmodel import Column, DateTime, Field, Relationship, func


# Password hashing for UserAccount
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAccount(
    rx.Model,
    table=True
):
    """A local UserAccount model with bcrypt password hashing."""

    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    email: str = Field(nullable=False, unique=True, index=True)
    password_hash: str = Field(nullable=False)
    profile_text: str = Field(nullable=True)
    profile_picture: str = Field(nullable=True)
    enabled: bool = Field(default=True)

    # Foreign Keys
    city_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "city.id",
                name="fk_useraccount_city_id_city",
            ),
            index=True,
            nullable=False,
        ),
    )

    # Relationships
    city: "City" = Relationship(
        back_populates="useraccount_list"
    )
    interest_list: Optional[list["UserInterest"]] = Relationship(
        back_populates="useraccount"
    )
    post_list: Optional[list["Post"]] = Relationship(
        back_populates="useraccount"
    )
    comment_list: Optional[list["Comment"]] = Relationship(
        back_populates="useraccount"
    )
    user_private_message_sent_list: Optional[list["UserPrivateMessage"]] = (
        Relationship(
            back_populates="sender",
            sa_relationship_kwargs={
                "foreign_keys": "UserPrivateMessage.sender_id"
            }
        )
    )
    user_private_message_received_list: Optional[list["UserPrivateMessage"]] = (  # noqa: E501
        Relationship(
            back_populates="recipient",
            sa_relationship_kwargs={
                "foreign_keys": "UserPrivateMessage.recipient_id"
            }
        )
    )
    auth_session: "AuthSession" = Relationship(
        back_populates="useraccount"
    )

    @staticmethod
    def format_last_name(last_name: str) -> str:
        """
        Format the last name so the first letter and each letter
        after a '-' or a space are capitalized.
        """
        return ' '.join(
            '-'.join(part.capitalize() for part in segment.split('-'))
            for segment in last_name.split()
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
    useraccount_list: Optional[list["UserAccount"]] = Relationship(
        back_populates="city"
    )


class Interest(
    rx.Model,
    table=True
):
    """An Interest model."""

    name: str = Field(nullable=False)

    # Relationships
    useraccount_list: Optional[list["UserInterest"]] = Relationship(
        back_populates="interest"
    )


class UserInterest(
    rx.Model,
    table=True
):
    """A model to join User and his Interest(s)."""

    # Foreign keys
    useraccount_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "useraccount.id",
                name="fk_userinterest_useraccount_id_useraccount",
            ),
            index=True,
            nullable=False,
        ),
    )
    interest_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "interest.id",
                name="fk_userinterest_interest_id_interest",
            ),
            index=True,
            nullable=False,
        ),
    )

    # Relationships
    useraccount: "UserAccount" = Relationship(
        back_populates="interest_list"
    )
    interest: "Interest" = Relationship(
        back_populates="useraccount_list"
    )


class Post(
    rx.Model,
    table=True
):
    """A Post model."""

    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published_at: datetime = Field(nullable=False)
    is_published: bool = Field(nullable=False, default=True)
    is_pinned: bool = Field(nullable=False, default=False)

    # Foreign keys
    author_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "useraccount.id",
                name="fk_post_author_id_useraccount",
            ),
            index=True,
            nullable=False,
        ),
    )
    category_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "postcategory.id",
                name="fk_post_category_id_postcategory",
            ),
            index=True,
            nullable=False,
            default=1,
        )
    )

    # Relationships
    useraccount: "UserAccount" = Relationship(
        back_populates="post_list"
    )
    postcategory: "PostCategory" = Relationship(
        back_populates="post_list"
    )
    comment_list: Optional[list["Comment"]] = Relationship(
        back_populates="post"
    )


class PostCategory(
    rx.Model,
    table=True
):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)

    # Relationships
    post_list: Optional[list["Post"]] = Relationship(
        back_populates="postcategory"
    )


class Comment(
    rx.Model,
    table=True
):
    """A Comment model."""

    content: str = Field(nullable=False)
    published_at: datetime = Field(nullable=False)
    is_published: bool = Field(nullable=False, default=True)

    # Foreign keys
    post_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "post.id",
                name="fk_comment_post_id_post",
            ),
            index=True,
            nullable=False,
        ),
    )
    author_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "useraccount.id",
                name="fk_comment_author_id_useraccount",
            ),
            index=True,
            nullable=False,
        ),
    )

    # Relationships
    post: "Post" = Relationship(
        back_populates="comment_list"
    )
    useraccount: "UserAccount" = Relationship(
        back_populates="comment_list"
    )


class PrivateMessage(
    rx.Model,
    table=True
):
    """A PrivateMessage model."""

    content: str = Field(nullable=False)
    published_at: datetime = Field(nullable=False)

    # Relationships
    user_private_message_list: Optional[list["UserPrivateMessage"]] = (
        Relationship(back_populates="private_message")
    )


class UserPrivateMessage(
    rx.Model,
    table=True
):
    """A UserPrivateMessage model to associate Users with PrivateMessages."""

    # Foreign keys
    sender_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "useraccount.id",
                name="fk_userprivatemessage_sender_id_useraccount",
            ),
            index=True,
            nullable=False,
        ),
    )
    recipient_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "useraccount.id",
                name="fk_userprivatemessage_recipient_id_useraccount",
            ),
            index=True,
            nullable=False,
        ),
    )
    private_message_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "privatemessage.id",
                name="fk_userprivatemessage_private_message_id_privatemessage",
            ),
            index=True,
            nullable=False,
        ),
    )
    is_read: bool = Field(nullable=False, default=False)

    # Relationships
    sender: "UserAccount" = Relationship(
        back_populates="user_private_message_sent_list",
        sa_relationship_kwargs={
            "foreign_keys": "UserPrivateMessage.sender_id"
        }
    )
    recipient: "UserAccount" = Relationship(
        back_populates="user_private_message_received_list",
        sa_relationship_kwargs={
            "foreign_keys": "UserPrivateMessage.recipient_id"
        }
    )
    private_message: "PrivateMessage" = Relationship(
        back_populates="user_private_message_list"
    )


class AuthSession(
    rx.Model,
    table=True,
):
    """Correlate a session_id with an arbitrary user_id."""

    session_id: str = Field(unique=True, index=True, nullable=False)
    expiration: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ),
    )

    # Foreign keys
    useraccount_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "useraccount.id",
                name="fk_authsession_useraccount_id_useraccount",
            ),
            index=True,
            nullable=False,
        ),
    )

    # Relationships
    useraccount: UserAccount = Relationship(
        back_populates="auth_session",
    )
