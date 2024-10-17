import reflex as rx

from ...components.interest_badges import interest_badges


def new_group_dialog() -> rx.Component:
    from ...pages.groups import GroupsState

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.text("Créer", font_weight='600'),
                width='100px',
                on_click=GroupsState.handle_dialog_open,
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Nouvelle Fratrie"),
            rx.hstack(
                rx.upload(
                    rx.image(
                        src=rx.get_upload_url(
                            GroupsState.new_group_image
                        ),
                        width=['7em'],
                        height=['7em'],
                        border_radius='50%',
                        object_fit="cover",
                    ),
                    id='profile_img',
                    multiple=False,
                    accept={
                        'image/png': ['.png'],
                        'image/jpeg': ['.jpg', '.jpeg'],
                    },
                    on_drop=GroupsState.handle_upload(
                        rx.upload_files(upload_id='group_img')
                    ),
                    padding='0',
                    width='7em',
                    height='7em',
                    border='none',
                ),
                rx.input(
                    max_length=20,
                    placeholder="Nom de la Fratrie",
                    size='3',
                    value=GroupsState.new_group_name,
                    on_change=GroupsState.set_new_group_name,
                ),
                justify='center',
                margin='0 0 1em',
                spacing='6',
            ),
            interest_badges(
                interests_names=GroupsState.interests_names,
                selected_interests_names=GroupsState.new_group_interest_name,
                add_selected=GroupsState.add_selected,
                remove_selected=GroupsState.remove_selected,
                badge_size='2',
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Annuler",
                        color_scheme="gray",
                        variant="soft",
                    ),
                ),
                rx.button(
                    "Créer",
                    on_click=GroupsState.create_group,
                    width='76px',
                ),
                justify="end",
                spacing="3",
                margin_top="1.5em",
            ),
        ),
    ),
