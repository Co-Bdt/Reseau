# import reflex as rx
# from sqlmodel import Field, Relationship

# from .user_account import UserAccount
# from .interest import Interest


# class UserInterest(
#     rx.Model,
#     table=True
# ):
#     """A model to join User and his Interest(s)."""

#     # Foreign keys
#     user_id: int = Field(nullable=False, foreign_key="useraccount.id")
#     interest_id: int = Field(nullable=False, foreign_key="interest.id")

#     # Relationships
#     user: "UserAccount" = Relationship(
#         back_populates="interest_list"
#     )
#     interest: "Interest" = Relationship(
#         back_populates="user_list"
#     )
