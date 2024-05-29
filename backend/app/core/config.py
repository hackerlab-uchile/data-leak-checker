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
