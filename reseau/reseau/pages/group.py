import reflex as rx
import sqlalchemy as sa

from ..common.base_state import BaseState
from ..common.template import template
from ..models import Group, UserGroup
from ..reseau import GROUPS_ROUTE


class GroupState(rx.State):

    async def init(self):
        ...


@rx.page(
    title="Fratries",
    route=f'{GROUPS_ROUTE}/[name]',
    on_load=GroupState.init
)
@template
def group_page():
    return rx.cond(
        GroupState.is_hydrated,
        rx.hstack(
            rx.vstack(
                rx.text("Les techos"),
                width='85%'
            ),
            rx.vstack(
                rx.text("Membres"),
                width='15%'
            ),
        )
    )
