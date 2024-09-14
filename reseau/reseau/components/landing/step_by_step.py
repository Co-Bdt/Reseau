import reflex as rx


def step_one() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Étape 1",
            style=rx.Style(
                color='#FFC53D',
                font_weight="700",
                font_size='0.75em',
                font_family='Inter, sans-serif',
            ),
        ),
        rx.text(
            "Crée ton profil",
            style=rx.Style(
                color='white',
                font_weight="700",
                font_size=['1.75em', '2em', '2.25em', '2.75em'],
                font_family='Inter, sans-serif',
            ),
        ),
        rx.text(
            rx.hstack(
                rx.icon('circle-check'),
                "Indique ta localisation",
            ),
            rx.hstack(
                rx.icon('circle-check'),
                "Affiche tes intérêts",
                style=rx.Style(
                    margin_top='0.5em',
                ),
            ),
            style=rx.Style(
                margin_top='0.5em',
                color='white',
                font_family='Satoshi Variable, sans-serif',
            ),
        ),
        spacing='0',
    )


def step_two() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Étape 2",
            style=rx.Style(
                color='#FFC53D',
                font_weight="700",
                font_size='0.75em',
                font_family='Inter, sans-serif',
            ),
        ),
        rx.text(
            "Présente toi",
            style=rx.Style(
                color='white',
                font_weight="700",
                font_size=['1.75em', '2em', '2.25em', '2.75em'],
                font_family='Inter, sans-serif',
            ),
        ),
        rx.text(
            "Partage ton histoire, tes ambitions",
            rx.text("et discute avec d'autres gars."),
            style=rx.Style(
                margin_top='0.5em',
                color='white',
                font_family='Satoshi Variable, sans-serif',
            ),
        ),
        spacing='0',
    )


def step_by_step() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.desktop_only(
                rx.hstack(
                    rx.image(
                        src="/image_etape1.png",
                        style=rx.Style(
                            radius='0.75em',
                        ),
                    ),
                    step_one(),
                    spacing='9',
                    justify='between',
                ),
                rx.hstack(
                    step_two(),
                    rx.image(
                        src="/image_etape2.png",
                        style=rx.Style(
                            radius='0.75em',
                        ),
                    ),
                    spacing='9',
                    justify='between',
                    style=rx.Style(
                        margin_top='5em',
                    ),
                ),
            ),
            rx.mobile_and_tablet(
                rx.vstack(
                    step_one(),
                    rx.image(
                        src="/image_etape1.png",
                        style=rx.Style(
                            radius='0.75em',
                        ),
                    ),
                    rx.spacer(
                        style=rx.Style(
                            height='1em',
                        ),
                    ),
                    step_two(),
                    rx.image(
                        src="/image_etape2.png",
                        style=rx.Style(
                            radius='0.75em',
                        ),
                    ),
                    spacing='5',
                ),
            ),
            align='center',
        ),
        size='4',
        padding='0',
        padding_x='1.25em',
        padding_y=['2.5em', '3em', '4em'],
        style=rx.Style(
            width='100%',
            background_color='#020200',
        ),
    ),
