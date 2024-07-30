import reflex as rx

from ..models import Interest


class UserCard(rx.ComponentState):

    def interest_chip(interest: Interest) -> rx.Component:
        return rx.badge(
            interest.name,
            color_scheme="amber",
            radius="full",
            variant="surface",
        )

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        user = props.pop("user")
        city = props.pop("city")
        is_profile_empty = props.pop("is_profile_empty", True)
        interest_list: list[Interest] = props.pop("interest_list", [])

        return rx.card(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.image(
                            src=rx.get_upload_url(
                                f"{user.id}_profile_picture"
                            ),
                            width="4.5vh",
                            height="4.5vh",
                            border="0.5px solid #ccc",
                            border_radius="50%",
                        ),
                        rx.vstack(
                            rx.text(
                                f"{user.username}",
                                size="2",
                                weight="medium",
                            ),
                            rx.text(
                                f"{city.name} ({city.postal_code})",
                                size="2",
                                color_scheme="gray",
                            ),
                            spacing="1",
                        ),
                        width="100%",
                        align="start",
                    ),
                    rx.hstack(
                        rx.foreach(
                            interest_list,
                            UserCard.interest_chip,
                        ),
                        spacing="1",
                    ),
                    rx.text(
                        f"{user.email}",
                        size="2",
                        color_scheme="gray",
                    ),
                    rx.box(
                        rx.cond(
                            is_profile_empty,
                            rx.text(
                                "Aucune description",
                                size="2",
                                color_scheme="gray",
                                style={
                                    "font-style": "italic",
                                },
                            ),
                            rx.text(
                                f"{user.profile_text}",
                                size="2",
                                style={
                                    "line-height": "1.4",
                                    "letter-spacing": "0.2px",
                                },
                            ),
                        ),
                        margin="0.5em 0 0 0"
                    ),
                ),
                # width=["100%", "49.1%", "32.2%", "32.2%", "24.1%"],
            ),
            as_child=True,
            size="3",
        )


user_card = UserCard.create


# @rx.page(on_load=UserCardState.init)
# def user_card(
#     user: UserAccount,
#     city: City,
#     is_profile_empty: bool
# ) -> rx.Component:
#     """
#     Display a user card with the user's profile picture,
#     username, city, interests, email, and profile text.

#     Returns:
#         A Reflex Component: The user card.
#     """
#     # UserCardState.set_user(user)
#     # UserCardState.set_city(city)
#     # UserCardState.set_interests(interests)
#     # UserCardState.set_is_profile_empty(is_profile_empty)

#     return rx.card(
#         rx.box(
#             rx.vstack(
#                 rx.hstack(
#                     rx.image(
#                         src=rx.get_upload_url(f"{user.id}_profile_picture"),
#                         width="4vh",
#                         height="4vh",
#                         border="1px solid #ccc",
#                         border_radius="50%",
#                     ),
#                     rx.vstack(
#                         rx.text(
#                             f"{user.username}",
#                             size="2",
#                             weight="medium",
#                         ),
#                         rx.text(
#                             f"{city.name} ({city.postal_code})",
#                             size="2",
#                             color_scheme="gray",
#                             # style={"text-"}
#                         ),
#                         # spacing="0",
#                     ),
#                     width="100%",
#                     align="start",
#                 ),
#                 rx.foreach(
#                     UserCardState.interests_names,
#                     selected_item_chip,
#                 ),
#                 # rx.text(
#                 #     "Intérêts",
#                 #     size="2",
#                 #     color_scheme="gray",
#                 # ),
#                 rx.text(
#                     f"{user.email}",
#                     size="2",
#                     color_scheme="gray",
#                 ),
#                 rx.box(
#                     rx.cond(
#                         is_profile_empty,
#                         rx.text(
#                             "Aucune description",
#                             size="2",
#                             color_scheme="gray",
#                             style={
#                                 "font-style": "italic",
#                             },
#                         ),
#                         rx.text(
#                             f"{user.profile_text}",
#                             size="2",
#                             style={
#                                 "line-height": "1.4",
#                                 "letter-spacing": "0.2px",
#                             },
#                         ),
#                     ),
#                     margin="1em 0 0 0"
#                 ),
#             ),
#             # width=["100%", "49.1%", "32.2%", "32.2%", "24.1%"],
#         ),
#         as_child=True,
#         size="3",
#     )
