from random import shuffle
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..models import Group, UserGroup
from ..reseau import GROUPS_ROUTE


class GroupsState(rx.State):
    public_groups_displayed: list[Group] = []
    user_groups_displayed: list[tuple[Group, str]] = []

    async def init(self):
        await self.load_groups()

    async def load_groups(self):
        # Public groups
        self.public_groups_displayed = []
        with rx.session() as session:
            groups = session.exec(
                Group.select()
                .options(
                    sa.orm.selectinload(Group.interest)
                )
            ).all()
        self.public_groups_displayed = groups
        # Display public groups in random order.
        shuffle(self.public_groups_displayed)

        # Groups the user is part of
        self.user_groups_displayed = []
        base_state = await self.get_state(BaseState)
        with rx.session() as session:
            usergroups = session.exec(
                Group.select()
                .join(UserGroup)
                .options(
                    sa.orm.selectinload(Group.interest)
                )
                .where(
                    UserGroup.useraccount_id ==
                    base_state.authenticated_user.id
                )
            ).all()
        self.user_groups_displayed = usergroups
        for group in usergroups:
            self.user_groups_displayed.append(
                (group, Group.url_name(group.name))
            )

    async def join_group(self, group: Group):
        base_state = await self.get_state(BaseState)

        usergroup = UserGroup(
            useraccount_id=base_state.authenticated_user.id,
            group_id=group['id']
        )
        with rx.session() as session:
            session.add(usergroup)
            session.commit()


@rx.page(title="Fratries", route=GROUPS_ROUTE, on_load=GroupsState.init)
@template
def groups_page() -> rx.Component:
    """
    Render the groups page which allow users to \
        - search for groups by interest
        - join a group

    Returns:
        A reflex component.
    """
    return rx.cond(
        GroupsState.is_hydrated,
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.text("Barre de recherche", width='100%'),
                    rx.text("Créer", width='100px')
                ),
                rx.desktop_only(
                    rx.grid(
                        rx.foreach(
                            GroupsState.public_groups_displayed,
                            lambda group: rx.card(
                                rx.box(
                                    rx.vstack(
                                        rx.text(group.name),
                                        rx.hstack(
                                            rx.text("X/5 membres"),
                                            rx.text(group.interest.name),
                                        ),
                                        rx.button(
                                            "Rejoindre",
                                            on_click=GroupsState.join_group(
                                                group
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        columns='3',
                    )
                ),
                # rx.tablet_only(
                # ),
                # rx.mobile_only(
                # ),
                width='85%',
            ),
            rx.vstack(
                rx.text("Mes Fratries"),
                rx.grid(
                    rx.foreach(
                        GroupsState.user_groups_displayed,
                        lambda group: rx.card(
                            rx.box(
                                rx.text(group[0].name),
                                rx.hstack(
                                    rx.text("X/5 membres"),
                                    rx.text(group[0].interest.name),
                                ),
                            ),
                            cursor='pointer',
                            on_click=rx.redirect(
                                f"{GROUPS_ROUTE}/{group[1]}"
                            ),
                        ),
                    ),
                    columns='1',
                ),
                justify='start',
                width='15%',
            )
        )
    )
