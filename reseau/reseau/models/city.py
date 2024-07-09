from sqlmodel import Field
import reflex as rx


class City(
    rx.Model,
    table=True,
):
    """A local City model."""

    name: str = Field(nullable=False)
    postal_code: str = Field(nullable=False)
