import reflex as rx

from .common.style import style


HOME_ROUTE = "/"
REGISTER_ROUTE = "/rejoindre"
LOGIN_ROUTE = "/connexion"
PROFILE_ROUTE = "/profil"
MEMBERS_ROUTE = "/membres"


app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="amber",
    ),
    style=style,  # Global style configuration
    stylesheets=[  # Specific stylesheets
        "/styles.css",  # This path is relative to assets/
    ],
)
