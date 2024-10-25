import reflex as rx

from ...components.common.interest_chip import interest_chip
from ...reseau import GROUPS_ROUTE


def public_groups_grid(
    column_nb: str = '2'
) -> rx.Component:
    from ...pages.groups import GroupsState

    return rx.grid(
        rx.foreach(
            GroupsState.public_groups_displayed,
            lambda group: rx.card(
                rx.box(
                    rx.image(
                        src=rx.get_upload_url(
                            group[0].image
                        ),
                        height='60%',
                        object_fit="cover",
                        width='100%',
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.hstack(
                                    rx.text(
                                        group[1],
                                        style=rx.Style(
                                            font_size='1.3em',
                                            font_weight='600',
                                            overflow='hidden',
                                            text_overflow='ellipsis',
                                            white_space='nowrap',
                                        ),
                                    ),
                                    interest_chip(
                                        group[0].interest
                                    ),
                                    justify='between',
                                    width='100%',
                                ),
                                rx.text(
                                    f"{group[2]}/"
                                    f"{group[0].max_members} membres",  # noqa
                                    style=rx.Style(
                                        color='gray',
                                        font_size='0.8em',
                                    )
                                ),
                                spacing='1',
                                width='100%',
                            ),
                            width='100%',
                        ),
                        rx.cond(
                            ~group[3],
                            rx.button(
                                "Rejoindre",
                                on_click=GroupsState.join_group(  # noqa
                                    group[0]
                                ),
                            ),
                            rx.button(
                                "Ouvrir",
                                on_click=rx.redirect(
                                    f"{GROUPS_ROUTE}/{group[0].name}"  # noqa
                                ),
                            ),
                        ),
                        height='40%',
                        padding='1em',
                        width='100%',
                    ),
                    height='100%',
                ),
                padding='0',
                height='340px',
            ),
        ),
        columns=column_nb,
        spacing='6',
        width='100%',
    ),
