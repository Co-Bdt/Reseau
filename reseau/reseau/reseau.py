import reflex as rx


HOME_ROUTE = "/"
REGISTER_ROUTE = "/rejoindre"
LOGIN_ROUTE = "/connexion"
PROFILE_ROUTE = "/profil"
MEMBERS_ROUTE = "/membres"

S3_BUCKET_NAME = "reseau-images-bucket"


app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="amber",
    )
)
