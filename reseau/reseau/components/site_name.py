import reflex as rx


def site_name(
    color: str = 'black',
    **props,
):
    return rx.fragment(
        rx.desktop_only(
            rx.link(
                'Reseau',
                href='/',
                underline='none',
                size='7',
                color=color,
                style=rx.Style(
                    font_weight='700',
                    font_family='Inter, sans-serif',
                    kwargs=props,
                ),
            ),
            width='100%',
            margin='0',
        ),
        rx.mobile_and_tablet(
            rx.link(
                'Reseau',
                href='/',
                underline='none',
                size='6',
                color=color,
                style=rx.Style(
                    font_weight='700',
                    font_family='Inter, sans-serif',
                    kwargs=props,
                ),
            ),
            width='100%',
            margin='0',
        ),
        justify='start',
    )
