from typing import Tuple
import reflex as rx

from ..components.user_hover_card import user_hover_card
from ..models import (
    City,
    Interest,
    UserAccount,
)
from .profile_picture import profile_picture


class MembersGrid(rx.ComponentState):

    def interest_chip(interest: Interest) -> rx.Component:
        return rx.badge(
            interest.name,
            color_scheme='amber',
            radius='full',
            variant='surface',
        )

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        users: list[Tuple[UserAccount, City, list[Interest]]] = (
            props.pop('users')
        )
        columns: int = props.pop('columns')

        return rx.grid(
            rx.foreach(
                users,
                lambda user: rx.card(
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.hover_card.root(
                                    rx.hover_card.trigger(
                                        rx.link(
                                            profile_picture(
                                                style=rx.Style(
                                                    width='2.7em',
                                                    height='2.7em',
                                                ),
                                                profile_picture=user[0].profile_picture,  # noqa: E501
                                            ),
                                        ),
                                    ),
                                    rx.hover_card.content(
                                        user_hover_card(
                                            user[0],
                                            user[1],
                                        ),
                                    ),
                                ),
                                rx.vstack(
                                    rx.hstack(
                                        rx.text(
                                            f"{user[0].first_name}",
                                            class_name='desktop-medium-text',
                                        ),
                                        rx.text(
                                            f"{user[0].last_name}",
                                            class_name='desktop-medium-text',
                                        ),
                                        spacing='1',
                                    ),
                                    rx.text(
                                        f"{user[1].name} "
                                        f"({user[1].postal_code})",
                                        class_name='discreet-text',
                                    ),
                                    spacing='1',
                                ),
                                width='100%',
                                align='start',
                            ),
                            rx.hstack(
                                rx.foreach(
                                    user[2],
                                    MembersGrid.interest_chip,
                                ),
                                spacing='1',
                            ),
                            rx.text(
                                f"{user[0].email}",
                                class_name='mobile-text',
                                color_scheme='gray',
                            ),
                            rx.box(
                                rx.cond(
                                    ~user[0].profile_text,
                                    rx.text(
                                        "Aucune description",
                                        class_name='mobile-text',
                                        color_scheme='gray',
                                        style={
                                            'font-style': 'italic',
                                        },
                                    ),
                                    rx.text(
                                        f"{user[0].profile_text}",
                                        class_name='mobile-text',
                                        style={
                                            'line-height': '1.4',
                                            'letter-spacing': '0.2px',
                                        },
                                    ),
                                ),
                                margin='0.5em 0 0 0'
                            ),
                        ),
                    ),
                    as_child=True,
                    size='3',
                ),
            ),
            columns=columns,
            width='100%',
            spacing='3',
            flex_wrap='wrap',
        )


members_grid = MembersGrid.create
