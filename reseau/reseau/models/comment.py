# from datetime import datetime
# from sqlmodel import Field, Relationship
# import reflex as rx

# from .user_account import Post, UserAccount


# class Comment(
#     rx.Model,
#     table=True
# ):
#     """A Comment model."""

#     content: str = Field(nullable=False)
#     published_at: datetime = Field(nullable=False)
#     published: bool = True

#     # Foreign keys
#     post_id: int = Field(nullable=False, foreign_key="post.id")
#     author_id: int = Field(nullable=False, foreign_key="useraccount.id")

#     # Relationships
#     post: "Post" = Relationship(
#         back_populates="comments"
#     )
#     user_account: "UserAccount" = Relationship(
#         back_populates="comments"
#     )

#     @staticmethod
#     def format_datetime(dt: datetime) -> str:
#         """Format a datetime for display."""
#         return dt.strftime("%Y-%m-%d %H:%M:%S")
