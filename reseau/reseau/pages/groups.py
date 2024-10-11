from random import shuffle
import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..models import Group, UserGroup
from ..reseau import GROUPS_ROUTE


class GroupsState(rx.State):
    public_groups_displayed: list[tuple[Group, str, int]] = []
    user_groups_displayed: list[tuple[Group, str, int]] = []

    async def init(self):
        await self.load_groups()

    async def load_groups(self):
        # Public groups
        self.public_groups_displayed = []
        with rx.session() as session:
            public_groups = session.exec(
                Group.select()
                .options(
                    sa.orm.selectinload(Group.interest),
                    sa.orm.selectinload(Group.user_group_list)
                    .selectinload(UserGroup.useraccount)
                )
            ).all()
        # self.public_groups_displayed = public_groups

        for group in public_groups:
            self.public_groups_displayed.append(
                (group,
                 Group.from_url_name(group.name),
                 len(group.user_group_list))
            )
        # Display public groups in random order.
        shuffle(self.public_groups_displayed)

        # Groups the user is part of
        self.user_groups_displayed = []
        base_state = await self.get_state(BaseState)
        with rx.session() as session:
            user_groups = session.exec(
                Group.select()
                .join(UserGroup)
                .options(
                    sa.orm.selectinload(Group.interest),
                    sa.orm.selectinload(Group.user_group_list)
                    .selectinload(UserGroup.useraccount)
                )
                .where(
                    UserGroup.useraccount_id ==
                    base_state.authenticated_user.id
                )
            ).all()

        for group in user_groups:
            self.user_groups_displayed.append(
                (group,
                 Group.from_url_name(group.name),
                 len(group.user_group_list))
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
        return rx.redirect(f"{GROUPS_ROUTE}/{group['name']}")


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
                    rx.button("Créer", width='100px')
                ),
                rx.desktop_only(
                    rx.grid(
                        rx.foreach(
                            GroupsState.public_groups_displayed,
                            lambda group: rx.card(
                                rx.box(
                                    rx.vstack(
                                        rx.text(group[1]),
                                        rx.hstack(
                                            rx.text(
                                                f"{group[2]}/{group[0].max_members} membres"
                                            ),
                                            rx.text(group[0].interest.name),
                                        ),
                                        rx.button(
                                            "Rejoindre",
                                            on_click=GroupsState.join_group(
                                                group[0]
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
                                rx.text(group[1]),
                                rx.hstack(
                                    rx.text(
                                        f"{group[2]}/{group[0].max_members} membres"
                                    ),
                                    rx.text(group[0].interest.name),
                                ),
                            ),
                            cursor='pointer',
                            on_click=rx.redirect(
                                f"{GROUPS_ROUTE}/{group[0].name}"
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
