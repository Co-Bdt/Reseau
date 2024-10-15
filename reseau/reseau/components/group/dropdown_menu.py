import reflex as rx


def button_item(
    content,
    func: callable = None
) -> rx.Component:
    return rx.button(
        content,
        on_click=func,
        variant='soft',
        style=rx.Style(
            background='transparent',
            color='black',
            _hover={
                'bg': rx.color('gray', 4),
            },
            cursor='pointer',
        ),
    )


def dropdown_menu():
    """
    Dropdown menu with the following options:
    (Members only)
    - Leave group
    (Owner only)
    - Edit group
    - Delete group
    """
    from ...pages.group import GroupState

    return rx.menu.root(
        rx.menu.trigger(
            rx.icon_button(
                rx.icon('ellipsis'),
                size='3', variant='soft',
                style=rx.Style(
                    background='transparent',
                    color='black',
                    _hover={
                        'bg': rx.color('gray', 4),
                    },
                    cursor='pointer',
                ),
            )
        ),
        rx.cond(
            GroupState.is_current_user_owner,
            rx.menu.content(
                rx.dialog.root(
                    rx.dialog.trigger(
                        button_item(
                            "Gérer les membres",
                            GroupState.handle_dialog_open
                        )
                    ),
                    rx.dialog.content(
                        rx.dialog.title(
                            "Gérer les membres",
                            margin='0 0 1em'
                        ),
                        rx.foreach(
                            GroupState.members_before_rm,
                            lambda member: rx.cond(
                                ~member.is_owner,
                                rx.card(
                                    rx.hstack(
                                        rx.text(
                                            f"{member.useraccount.first_name} ",
                                            f"{member.useraccount.last_name}",
                                            font_size='1.1em'
                                        ),
                                        # rx.icon_button(
                                        #     rx.icon('x'),
                                        #     on_click=GroupState
                                        #     .mark_member_to_remove(
                                        #         member
                                        #     ),
                                        # ),
                                        button_item(
                                            rx.icon('x', color='red'),
                                            GroupState.mark_member_to_remove(
                                                member
                                            )
                                        ),
                                        justify='between'
                                    ),
                                ),
                            ),
                        ),
                        rx.flex(
                            rx.dialog.close(
                                rx.button(
                                    "Annuler",
                                    color_scheme="gray",
                                    variant="soft",
                                ),
                            ),
                            rx.dialog.close(
                                rx.button(
                                    "Valider",
                                    on_click=GroupState.remove_members,
                                ),
                            ),
                            justify="end",
                            spacing="3",
                            margin_top="1.5em",
                        ),
                        max_width='400px'
                    ),
                ),
                rx.menu.separator(),
                rx.dialog.root(
                    rx.dialog.trigger(
                        button_item(
                            "Modifier la Fratrie"
                        )
                    ),
                    rx.dialog.content(
                        rx.dialog.title("Modifier la Fratrie"),
                        rx.upload(
                            rx.image(
                                src=rx.get_upload_url(
                                    GroupState.image
                                ),
                                width=['5em'],
                                height=['5em'],
                                border_radius='50%',
                                object_fit="cover",
                            ),
                            id='profile_img',
                            multiple=False,
                            accept={
                                'image/png': ['.png'],
                                'image/jpeg': ['.jpg', '.jpeg'],
                            },
                            on_drop=GroupState.handle_upload(
                                rx.upload_files(upload_id='group_img')
                            ),
                            padding='0',
                            width='6em',
                            height='5em',
                            border='none',
                        ),
                        rx.flex(
                            rx.dialog.close(
                                rx.button(
                                    "Annuler",
                                    color_scheme="gray",
                                    variant="soft",
                                ),
                            ),
                            rx.dialog.close(
                                rx.button(
                                    "Valider",
                                    on_click=GroupState.edit_group,
                                ),
                            ),
                            justify="end",
                            spacing="3",
                            margin_top="16px",
                        ),
                    ),
                ),
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        button_item(
                            "Dissoudre la Fratrie"
                        )
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Dissoudre la Fratrie"),
                        rx.alert_dialog.description(
                            "Veux-tu vraiment dissoudre cette Fratrie ?\n"
                            "Toutes les données seront perdues."
                        ),
                        rx.flex(
                            rx.alert_dialog.cancel(
                                rx.button("Annuler"),
                            ),
                            rx.alert_dialog.action(
                                rx.button(
                                    "Dissoudre",
                                    on_click=GroupState.delete_group
                                ),
                            ),
                            justify='end',
                            spacing='3',
                        ),
                    ),
                ),
                align_items='start'
            ),
            rx.menu.content(
                rx.menu.item(
                    button_item(
                        "Quitter la Fratrie",
                        GroupState.quit_group
                    ),
                ),
                align_items='start'
            ),
        ),
    )
