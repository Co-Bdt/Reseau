import os
import reflex as rx


APP_IP = os.environ.get("APP_IP", "0.0.0.0")

BACK_PORT = os.environ.get("BACK_PORT", "8000")

LOCAL_SQLITE_URL = "sqlite:///reseau.db"
AMAZON_RDS_POSTGRESQL_URL = os.environ.get(
    "AMAZON_RDS_POSTGRESQL_URL",
    LOCAL_SQLITE_URL
)

GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

DEV_S3_BUCKET_NAME = "dev-reseau-images-bucket"
S3_BUCKET_NAME = os.environ.get(
    "S3_BUCKET_NAME",
    DEV_S3_BUCKET_NAME
)

config = rx.Config(
    app_name="reseau",
    api_url=f"http://{APP_IP}:{BACK_PORT}",
    db_url=AMAZON_RDS_POSTGRESQL_URL,
)
