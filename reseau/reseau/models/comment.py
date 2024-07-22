from datetime import datetime
from sqlmodel import Field
import reflex as rx


class Comment(
    rx.Model,
    table=True
):
    """A Comment model."""

    content: str = Field(nullable=False)
    post_id: int = Field(nullable=False)
    author_id: int = Field(nullable=False)
    published_at: datetime = Field(nullable=False)
    published: bool = True

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format a datetime for display."""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
