import reflex as rx


chip_props = {
    'radius': 'full',
    'variant': 'surface',
    'cursor': 'pointer',
    'style': {
        '_hover': {'opacity': 0.75},
        'font_family': 'Satoshi Variable, sans-serif',
    },
}


def interest_badges(
    interests_names: list[str],
    selected_interests_names: list[str],
    add_selected: callable,
    remove_selected: callable,
    badge_size: str,
) -> rx.Component:

    def selected_item_chip(item: str) -> rx.Component:
        return rx.badge(
            item,
            rx.icon('circle-x', size=18),
            size=badge_size,
            color_scheme='green',
            **chip_props,
            on_click=remove_selected(item),
        )

    def unselected_item_chip(item: str) -> rx.Component:
        return rx.cond(
            selected_interests_names.contains(item),
            rx.fragment(),
            rx.badge(
                item,
                rx.icon('circle-plus', size=18),
                size=badge_size,
                color_scheme='gray',
                **chip_props,
                on_click=add_selected(item),
            ),
        )

    return rx.vstack(
        # Selected Items
        rx.flex(
            # Hidden badge to reserve space
            rx.badge(
                "Hidden",
                rx.icon('circle-x', size=18),
                size=badge_size,
                **chip_props,
                visibility='hidden',
                display=rx.cond(
                    selected_interests_names,
                    'none',
                    'flex',
                ),
            ),
            rx.foreach(
                selected_interests_names,
                selected_item_chip,
            ),
            wrap='wrap',
            spacing='2',
            justify_content='start',
        ),
        rx.divider(),

        # Unselected Items
        rx.flex(
            rx.foreach(
                interests_names,
                unselected_item_chip,
            ),
            wrap='wrap',
            spacing='2',
            justify_content='start',
        ),
        justify_content='start',
        align_items='start',
        width='100%',
    )
