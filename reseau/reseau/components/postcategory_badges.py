import reflex as rx

from ..models import PostCategory


badge_props = {
    'radius': 'full',
    'variant': 'surface',
    'size': '3',
    'cursor': 'pointer',
}

postcategory_all = PostCategory(
    id=0,
    name="Tous"
)


def postcategory_badges(
    postcategories: list[PostCategory],
    current_postcategory: int,
    on_change_current_postcategory: callable
) -> rx.Component:

    def selected_badge(postcategory: PostCategory) -> rx.Component:
        return rx.badge(
            postcategory.name,
            **badge_props,
            color='white',
            background='gray',
            box_shadow='inset 0 0 0 1px gray'
        )

    def unselected_badge(postcategory: PostCategory) -> rx.Component:
        return rx.badge(
            postcategory.name,
            color_scheme='gray',
            **badge_props,
            _hover={
                'color': 'white',
                'bg': 'gray'
            },
            on_click=on_change_current_postcategory(
                postcategory
            ),
        )

    return rx.flex(
        rx.cond(
            current_postcategory == postcategory_all.id,
            selected_badge(postcategory_all),
            unselected_badge(postcategory_all),
        ),
        rx.foreach(
            postcategories,
            lambda postcategory:
                rx.cond(
                    current_postcategory == postcategory.id,
                    selected_badge(postcategory),
                    unselected_badge(postcategory),
                )
        ),
        direction='row',
        spacing='2',
        margin_y='0.75em'
    )
