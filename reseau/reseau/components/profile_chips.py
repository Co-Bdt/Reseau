import reflex as rx

from ..models.user_account import Interest


chip_props = {
    "radius": "full",
    "variant": "surface",
    "size": "3",
    "cursor": "pointer",
    "style": {"_hover": {"opacity": 0.75}},
}


class ProfileChips(rx.ComponentState):
    @classmethod
    def get_component(cls, **props):
        # Query all interests from the database
        interests_names: list[str] = []
        with rx.session() as session:
            interests = session.exec(
                Interest.select()
                .order_by(Interest.name.asc())
            ).all()
            interests_names = [interest.name for interest in interests]

        selected_items: list[str] = props.pop("selected_items", [])
        add_selected = props.pop("add_selected")
        remove_selected = props.pop("remove_selected")

        def selected_item_chip(item: str) -> rx.Component:
            return rx.badge(
                item,
                rx.icon("circle-x", size=18),
                color_scheme="green",
                **chip_props,
                on_click=remove_selected(item),
            )

        def unselected_item_chip(item: str) -> rx.Component:
            return rx.cond(
                selected_items.contains(item),
                rx.fragment(),
                rx.badge(
                    item,
                    rx.icon("circle-plus", size=18),
                    color_scheme="gray",
                    **chip_props,
                    on_click=add_selected(item),
                ),
            )

        return rx.vstack(
            rx.flex(
                rx.hstack(
                    rx.icon("hand-heart", size=20),
                    rx.heading(
                        "Intérêts"
                        + f" ({selected_items.length()})",
                        size="3",
                    ),
                    spacing="1",
                    align="center",
                    width="100%",
                    justify_content=["end", "start"],
                ),
                justify="between",
                flex_direction=["column", "row"],
                align="center",
                spacing="2",
                margin_bottom="10px",
                width="100%",
            ),
            # Selected Items
            rx.flex(
                rx.foreach(
                    selected_items,
                    selected_item_chip,
                ),
                wrap="wrap",
                spacing="2",
                justify_content="start",
            ),
            rx.divider(),
            # Unselected Items
            rx.flex(
                rx.foreach(
                    interests_names,
                    unselected_item_chip,
                ),
                wrap="wrap",
                spacing="2",
                justify_content="start",
            ),
            justify_content="start",
            align_items="start",
            width="100%",
        )


profile_chips = ProfileChips.create
