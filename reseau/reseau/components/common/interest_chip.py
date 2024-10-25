import reflex as rx

from ...models import Interest


def interest_chip(interest: Interest) -> rx.Component:
    return rx.badge(
        interest.name,
        color_scheme='amber',
        radius='full',
        variant='surface',
    )
