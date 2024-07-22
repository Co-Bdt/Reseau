from datetime import datetime
import reflex as rx


class Post(
    rx.Model,
    table=True
):
    """A Post model."""

    title: str
    content: str
    author_id: int
    published_at: datetime
    published: bool = True

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format a datetime for display."""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
