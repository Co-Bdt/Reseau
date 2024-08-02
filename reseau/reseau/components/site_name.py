import reflex as rx


class SiteName(rx.ComponentState):

    def press(self):
        print("Rɘseau")

    @classmethod
    def get_component(cls, **props):
        return rx.box(
            rx.desktop_only(
                rx.link(
                    "Reseau",
                    href="/",
                    underline="none",
                    size="7",
                    color=rx.color_mode_cond(
                        light="black",
                        dark="white",
                    ),
                    style=rx.Style(
                        font_weight="bold",
                        letter_spacing="1px",
                    ),
                ),
                width="100%",
                margin="0 0 3em 0",
            ),
            rx.mobile_and_tablet(
                rx.box(
                    rx.heading(
                        "Rɘseau",
                        size="7",
                        style={
                            "letter-spacing": "1px"
                        },
                    ),
                    width="100%",
                    justify="start",
                    margin="0 0 3em 0.5em",
                ),
            ),
            justify="start",
        )


site_name = SiteName.create
