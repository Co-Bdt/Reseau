import os
import reflex as rx


LOCAL_SQLITE_URL = "sqlite:///reseau.db"
AMAZON_RDS_POSTGRESQL_URL = "postgresql://postgres:5zjbhMflkRoTRhbEtKO3@reseau-db-instance.chsg2oummucl.eu-west-3.rds.amazonaws.com/reseau"  # noqa: E501

APP_IP = os.environ.get("APP_IP", "0.0.0.0")
BACK_PORT = os.environ.get("BACK_PORT", "8000")

config = rx.Config(
    app_name="reseau",
    api_url=f"http://{APP_IP}:{BACK_PORT}",
    db_url=AMAZON_RDS_POSTGRESQL_URL,
)
