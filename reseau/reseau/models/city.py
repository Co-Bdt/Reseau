# import reflex as rx
# from sqlmodel import Field, Relationship
# from typing import Optional


# class City(
#     rx.Model,
#     table=True,
# ):
#     """A local City model."""

#     name: str = Field(nullable=False)
#     postal_code: str = Field(nullable=False)

#     # Relationships
#     users: Optional[list["UserAccount"]] = Relationship(  # type: ignore
#         back_populates="city"
#     )
