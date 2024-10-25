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


def postcategory_filter(
    postcategories: list[PostCategory],
    current_badge: int,
    on_change: callable
) -> rx.Component:

    def selected_badge(postcategory: PostCategory) -> rx.Component:
        return rx.badge(
            postcategory.name,
            color='white',
            background='gray',
            box_shadow='inset 0 0 0 1px gray',
            **badge_props,
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
            on_click=on_change(
                postcategory
            ),
        )

    return rx.flex(
        rx.cond(
            current_badge == postcategory_all.id,
            selected_badge(postcategory_all),
            unselected_badge(postcategory_all),
        ),
        rx.foreach(
            postcategories,
            lambda postcategory:
                rx.cond(
                    current_badge == postcategory.id,
                    selected_badge(postcategory),
                    unselected_badge(postcategory),
                )
        ),
        direction='row',
        spacing='2',
        margin_y='0.75em'
    )
