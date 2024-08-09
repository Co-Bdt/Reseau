import os
import reflex as rx


APP_IP = os.environ.get("APP_IP", "0.0.0.0")

BACK_PORT = os.environ.get("BACK_PORT", "8000")

LOCAL_SQLITE_URL = "sqlite:///reseau.db"

# AMAZON_RDS_POSTGRESQL_URL = "postgresql://postgres:5zjbhMflkRoTRhbEtKO3@reseau-db-instance.chsg2oummucl.eu-west-3.rds.amazonaws.com/reseau"  # noqa
AMAZON_RDS_POSTGRESQL_URL = os.environ.get(
    "AMAZON_RDS_POSTGRESQL_URL",
    LOCAL_SQLITE_URL
)

# GMAIL_APP_PASSWORD = "xpic zpwf rvxx jqpt"
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# S3_BUCKET_NAME = "reseau-images-bucket"
S3_BUCKET_NAME = os.environ.get(
    "S3_BUCKET_NAME",
    "dev-reseau-images-bucket"
)

config = rx.Config(
    app_name="reseau",
    api_url=f"http://{APP_IP}:{BACK_PORT}",
    db_url=LOCAL_SQLITE_URL,
)
