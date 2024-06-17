import os

POSTGRES_USER: str | None = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD: str | None = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_SERVER: str | None = os.environ.get("POSTGRES_SERVER")
POSTGRES_DB: str | None = os.environ.get("POSTGRES_DB")
POSTGRES_TEST_DB: str | None = os.environ.get("POSTGRES_TEST_DB")
HMAC_KEY: str | None = os.environ.get("HMAC_KEY")
SMTP_USERNAME: str | None = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD: str | None = os.environ.get("SMTP_PASSWORD")
SMTP_SERVER: str | None = os.environ.get("SMTP_SERVER")
JWT_SECRET: str | None = os.environ.get("JWT_SECRET")
JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", default="")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_ACCOUNT_SID: str = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_SENDER_NUMBER: str = os.environ.get("TWILIO_SENDER_NUMBER", "")
TWILIO_SENDER_NUMBER: str = os.environ.get("TWILIO_SENDER_NUMBER", "")
DEV_RECEIVER_NUMBER: str = os.environ.get("DEV_RECEIVER_NUMBER", "")
IN_PROD: str = os.environ.get("IN_PROD", "false")
CLIENT_ID: str = os.environ.get("CLIENT_ID", "")
CLIENT_SECRET: str = os.environ.get("CLIENT_SECRET", "")

# TODO: Lanzar errores cuando no se encuentren ciertos parámetors OBLIGATORIOS
