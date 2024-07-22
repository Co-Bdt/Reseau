import reflex as rx


def site_name() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.center(
                rx.heading(
                    "Rɘseau",
                    size="8",
                    style={
                        "font-family": "Droid Sans Mono",
                        "letter-spacing": "1px"
                    },
                ),
                width="100%",
                margin="0 0 3em 0",
            ),
            width="100%",
        ),
        rx.mobile_and_tablet(
            rx.box(
                rx.heading(
                    "Rɘseau",
                    size="8",
                    style={
                        "font-family": "Droid Sans Mono",
                        "letter-spacing": "1px"
                    },
                ),
                width="100%",
                justify="start",
                margin="0 0 3em 0.5em",
            ),
        ),
    )