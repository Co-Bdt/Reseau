# import datetime
# from sqlmodel import Column, DateTime, Field, Relationship, func
# import reflex as rx

# import user_account as user_account_module


# class AuthSession(
#     rx.Model,
#     table=True,
# ):
#     """Correlate a session_id with an arbitrary user_id."""

#     user_id: int = Field(
#         index=True,
#         nullable=False,
#         foreign_key="useraccount.id"
#     )
#     session_id: str = Field(unique=True, index=True, nullable=False)
#     expiration: datetime.datetime = Field(
#         sa_column=Column(
#             DateTime(timezone=True),
#             server_default=func.now(),
#             nullable=False
#         ),
#     )

#     # Relationships
#     user_account: user_account_module.UserAccount = Relationship(
#         back_populates="auth_session",
#     )
