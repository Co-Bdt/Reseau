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


class PostCategoryBadgesState(rx.State):
    current_postcategory: int = 0

    def set_current_postcategory(self, postcategory: PostCategory):
        from reseau.pages.home import HomeState

        self.current_postcategory = postcategory['id']
        return HomeState.load_posts(postcategory['id'])


def postcategory_badges(
    postcategories: list[PostCategory]
) -> rx.Component:

    def selected_badge(postcategory: PostCategory) -> rx.Component:
        return rx.badge(
            postcategory.name,
            **badge_props,
            color='white',
            background='gray',
            border='1px gray'
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
            on_click=PostCategoryBadgesState.set_current_postcategory(
                postcategory
            ),
        )

    return rx.flex(
        rx.cond(
            PostCategoryBadgesState.current_postcategory == postcategory_all.id,  # noqa: E501
            selected_badge(postcategory_all),
            unselected_badge(postcategory_all),
        ),
        rx.foreach(
            postcategories,
            lambda postcategory:
                rx.cond(
                    PostCategoryBadgesState.current_postcategory == postcategory.id,  # noqa: E501
                    selected_badge(postcategory),
                    unselected_badge(postcategory),
                )
        ),
        direction='row',
        spacing='2',
        margin_y='0.75em'
    )
