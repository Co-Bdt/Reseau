import reflex as rx
from typing import Callable

from .custom.autosize import autosize_textarea
from ..components.profile_picture import profile_picture
from ..models import PostCategory, UserAccount


dialog_button_style = {
    'width': '100%',
    'size': '3',
    'variant': 'outline',
    'color_scheme': 'gray',
    'radius': 'large',
    'style': rx.Style(
        justify_content='start',
        background_color='white',
        font_family='Inter, sans-serif',
        font_size=['0.9em', '1em'],
        cursor='pointer',
    )
}

title_input_style = {
    'width': '100%',
    'size': '3',
    'variant': 'soft',
    'color_scheme': 'gray',
    'background_color': 'white',
    'color': 'black',
    'style': rx.Style(
        border='0.5px solid #ccc',
        font_family='Inter, sans-serif',
        font_size=['0.9em', '1em'],
    ),
}


class WritePostDialogState(rx.State):
    title: str = ''
    content: str = ''
    selected_category: str = ''

    def on_change_selected_category(self, category: str):
        self.selected_category = category

    def clear_fields(self):
        self.title = ''
        self.content = ''


def write_post_dialog(
    user: UserAccount,
    postcategories: list[PostCategory],
    publish_post: Callable
):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Écris quelque chose",
                **dialog_button_style,
            )
        ),
        rx.dialog.content(
            rx.form.root(
                rx.flex(
                    rx.hstack(
                        profile_picture(
                            style=rx.Style(
                                width='2.7em',
                                height='2.7em',
                            ),
                            profile_picture=user.profile_picture,
                        ),
                        rx.text(
                            user.first_name,
                            style=rx.Style(
                                font_family='Inter, sans-serif',
                                font_weight='500',
                                margin_left='0.5em',
                            ),
                        ),
                        rx.text(
                            user.last_name,
                            style=rx.Style(
                                font_family='Inter, sans-serif',
                                font_weight='500',
                            ),
                        ),
                        spacing='1',
                        margin_bottom='0.5em',
                    ),
                    rx.text(
                        "Titre",
                        style=rx.Style(
                            color='#64748B',
                            font_family='Inter, sans-serif',
                            font_size='0.8em',
                            margin_top='1em',
                        ),
                    ),
                    rx.input(
                        name='title',
                        value=WritePostDialogState.title,
                        on_change=WritePostDialogState.set_title,
                        **title_input_style,
                    ),
                    rx.text(
                        "Contenu",
                        style=rx.Style(
                            color='#64748B',
                            font_family='Inter, sans-serif',
                            font_size='0.8em',
                            margin_top='1em',
                        ),
                    ),
                    autosize_textarea(
                        id='content',
                        class_name='autosize-textarea-post',
                        font_family='Inter, sans-serif',
                        font_size=['0.9em', '1em'],
                    ),
                    direction='column',
                    spacing='2',
                ),
                rx.flex(
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Choisis un canal",
                            radius='full',
                            style=rx.Style(
                                padding='1em',
                                box_shadow='none',
                                font_weight='500',
                                font_family='Inter, sans-serif',
                                _hover={
                                    'bg': '#f1f0ef',
                                },
                            )
                        ),
                        rx.select.content(
                            rx.foreach(
                                postcategories,
                                lambda postcategory: rx.select.item(
                                    rx.text(
                                        postcategory.name,
                                        style=rx.Style(
                                            font_family='Inter, sans-serif',
                                            font_weight='500',
                                            font_size='1.1em',
                                        ),
                                    ),
                                    value=postcategory.name,
                                ),
                            ),
                            position='popper',
                            side='bottom',
                            align='start',
                        ),
                        name='category',
                        value=WritePostDialogState.selected_category,
                        on_change=WritePostDialogState.on_change_selected_category,  # noqa: E501
                    ),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                rx.text(
                                    "Annuler",
                                    font_family='Inter, sans-serif'
                                ),
                                color_scheme='gray',
                                variant='soft',
                            ),
                        ),
                        rx.cond(
                            WritePostDialogState.title &
                            WritePostDialogState.selected_category,
                            rx.dialog.close(
                                rx.form.submit(
                                    rx.button(
                                        rx.text(
                                            "Publier",
                                            font_family='Inter, sans-serif',
                                        ),
                                        type='submit',
                                        on_click=WritePostDialogState.clear_fields,  # noqa: E501
                                    ),
                                ),
                            ),
                            rx.button(
                                rx.text(
                                    "Publier",
                                    font_family='Inter, sans-serif'
                                ),
                                disabled=True,
                            ),
                        ),
                        spacing='3',
                    ),
                    margin_top='16px',
                    justify_content='space-between',
                ),
                on_submit=publish_post,
                reset_on_submit=True,
            ),
            padding=['1em', '1.5em'],
        ),
    )
