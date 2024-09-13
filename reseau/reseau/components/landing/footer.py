import reflex as rx

from reseau.components.site_name import site_name


def footer(
    handle_email_change: rx.EventHandler,
    is_email_empty: bool,
    handle_submit: rx.EventHandler,
) -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Tu as des questions ?",
                    style=rx.Style(
                        color='white',
                        font_weight="600",
                        font_size=['1.5em', '1.75em', '2.25em', '2.75em'],
                        font_family='Inter, sans-serif',
                    ),
                ),
                rx.link(
                    rx.button(
                        rx.text(
                            "Contacte-nous",
                            style=rx.Style(
                                font_family='Inter, sans-serif',
                            ),
                        ),
                        size='2',
                        color_scheme='gray',
                        style=rx.Style(
                            width='9em',
                        ),
                    ),
                    href="mailto:contact-reseaudevperso@gmail.com",
                ),
                justify='between',
                width='100%',
            ),
            rx.form.root(
                rx.vstack(
                    rx.text(
                        "Tu souhaites être notifié des "
                        "prochaines mises à jours majeures ? ",
                        "(pas de spam, promis)",
                        style=rx.Style(
                            color='white',
                            font_size='0.9em',
                            font_family='Inter, sans-serif',
                        ),
                    ),
                    rx.hstack(
                        rx.input(
                            id='email',  # for the set_focus event
                            name='email',  # for the form_data
                            placeholder="Ton email",
                            on_change=handle_email_change,
                            style=rx.Style(
                                width='20em',
                            ),
                        ),
                        rx.cond(
                            is_email_empty,
                            rx.button(
                                rx.text(
                                    "Envoyer",
                                    style=rx.Style(
                                        font_family='Inter, sans-serif',
                                    ),
                                ),
                                disabled=True,
                                style=rx.Style(
                                    background_color='gray',
                                ),
                            ),
                            rx.form.submit(
                                rx.button(
                                    rx.text(
                                        "Envoyer",
                                        style=rx.Style(
                                            font_family='Inter, sans-serif',  # noqa: E501
                                        ),
                                    ),
                                    type='submit',
                                ),
                            ),
                        ),
                    ),
                    direction='column',
                    spacing='4',
                ),
                on_submit=handle_submit,
                reset_on_submit=True,
                style=rx.Style(
                    margin_top='2em',
                ),
            ),
            rx.box(
                style=rx.Style(
                    width='100%',
                    height='1px',
                    background_color='rgba(255, 255, 255, 0.2)',
                    margin_top='2em',
                    margin_bottom='1em',
                ),
            ),
            # TODO: Add privacy policy in a hstack
            site_name(
                color='white',
            ),
            rx.text(
                "© 2024",
                style=rx.Style(
                    color='rgba(255, 255, 255, 0.5)',
                    font_size='0.9em',
                    font_family='Satoshi Variable, sans-serif',
                ),
            ),
            align_items='start',
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
