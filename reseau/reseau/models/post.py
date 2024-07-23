from datetime import datetime
import reflex as rx
from sqlmodel import Field


class Post(
    rx.Model,
    table=True
):
    """A Post model."""

    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    author_id: int = Field(nullable=False)
    published_at: datetime = Field(nullable=False)
    published: bool = True

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format a datetime for display."""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
