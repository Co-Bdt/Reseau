import reflex as rx


chip_props = {
    'radius': 'full',
    'variant': 'surface',
    'size': '3',
    'cursor': 'pointer',
    'style': {'_hover': {'opacity': 0.75}},
}


def interest_badges(
    interests_names: list[str],
    selected_interests_names: list[str],
    add_selected: callable,
    remove_selected: callable,
) -> rx.Component:

    def selected_item_chip(item: str) -> rx.Component:
        return rx.badge(
            item,
            rx.icon('circle-x', size=18),
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
                color_scheme='gray',
                **chip_props,
                on_click=add_selected(item),
            ),
        )

    return rx.vstack(
        rx.hstack(
            rx.heading(
                "Intérêts",
                margin='0',
            ),
            spacing='1',
            width='100%',
            margin_bottom='0.5em',
        ),

        # Selected Items
        rx.flex(
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
        margin_top='1em',
    )
