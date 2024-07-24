# from __future__ import annotations

# from datetime import datetime
# import reflex as rx
# from sqlmodel import Field, Relationship
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from .user_account import UserAccount


# class Post(
#     rx.Model,
#     table=True
# ):
#     """A Post model."""

#     title: str = Field(nullable=False)
#     content: str = Field(nullable=False)
#     author_id: int = Field(nullable=False, foreign_key="user_account.id")
#     published_at: datetime = Field(nullable=False)
#     published: bool = True

#     # Relationships
#     user_account: "UserAccount" = Relationship(
#         back_populates="posts"
#     )

#     @staticmethod
#     def format_datetime(dt: datetime) -> str:
#         """Format a datetime for display."""
#         return dt.strftime("%Y-%m-%d %H:%M:%S")
