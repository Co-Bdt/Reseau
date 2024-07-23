import reflex as rx
from sqlmodel import Field


class Interest(
    rx.Model,
    table=True
):
    """An Interest model."""

    name: str = Field(nullable=False)
