import reflex as rx

from ...models import Interest


badge_props = rx.Style(
    radius='full',
    variant='surface',
)

desktop_badge_props = rx.Style(
    **badge_props,
    size='3',
)

mobile_badge_props = rx.Style(
    **badge_props,
    size='2',
)

interest_all = Interest(
    id=0,
    name="Tous"
)


class GroupInterestFilterState(rx.State):
    is_flex_expanded: bool = False

    def toggle_flex_expanded(self):
        self.is_flex_expanded = not self.is_flex_expanded


def group_interest_filter(
    group_interests: list[Interest],
    current_badge: int,
    on_change: callable
) -> rx.Component:

    def selected_badge(interest: Interest) -> rx.Component:
        return rx.fragment(
            rx.tablet_and_desktop(
                rx.badge(
                    interest.name,
                    color='white',
                    background='gray',
                    box_shadow='inset 0 0 0 1px gray',
                    **desktop_badge_props,
                )
            ),
            rx.mobile_only(
                rx.badge(
                    interest.name,
                    color='white',
                    background='gray',
                    box_shadow='inset 0 0 0 1px gray',
                    **mobile_badge_props,
                )
            )
        )

    def unselected_badge(interest: Interest) -> rx.Component:
        return rx.fragment(
            rx.tablet_and_desktop(
                rx.badge(
                    interest.name,
                    color='#909090',
                    color_scheme='gray',
                    **desktop_badge_props,
                    _hover={
                        'color': 'white',
                        'bg': 'gray'
                    },
                    on_click=on_change(
                        interest
                    ),
                )
            ),
            rx.mobile_only(
                rx.badge(
                    interest.name,
                    color='#909090',
                    color_scheme='gray',
                    **mobile_badge_props,
                    _hover={
                        'color': 'white',
                        'bg': 'gray'
                    },
                    on_click=on_change(
                        interest
                    ),
                )
            )
        )

    def util_badge(content: str, is_mobile: bool = False) -> rx.Component:
        return rx.badge(
            content,
            clickable=False,
            color_scheme='gray',
            color='#909090',
            **mobile_badge_props if is_mobile else desktop_badge_props,
            _hover={
                'color': 'white',
                'bg': 'gray'
            },
            on_click=GroupInterestFilterState.toggle_flex_expanded
        )

    return rx.hstack(
        rx.flex(
            rx.cond(
                current_badge == interest_all.id,
                selected_badge(interest_all),
                unselected_badge(interest_all),
            ),
            rx.foreach(
                group_interests,
                lambda interest:
                    rx.cond(
                        current_badge == interest.id,
                        selected_badge(interest),
                        unselected_badge(interest),
                    )
            ),
            direction='row',
            height=rx.cond(
                GroupInterestFilterState.is_flex_expanded,
                'auto',
                '2em'
            ),
            overflow=rx.cond(
                GroupInterestFilterState.is_flex_expanded,
                'visible',
                'hidden'
            ),
            spacing='2',
            wrap='wrap',
        ),
        rx.cond(
            GroupInterestFilterState.is_flex_expanded,
            rx.fragment(
                rx.tablet_and_desktop(
                    util_badge("Moins..."),
                ),
                rx.mobile_only(
                    util_badge("Moins...", is_mobile=True),
                ),
            ),
            rx.fragment(
                rx.tablet_and_desktop(
                    util_badge("Plus..."),
                ),
                rx.mobile_only(
                    util_badge("Plus...", is_mobile=True),
                ),
            ),
        ),
        spacing='2',
        align_items='start',
    )
