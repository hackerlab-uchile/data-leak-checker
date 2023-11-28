import os

POSTGRES_USER: str | None = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD: str | None = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_SERVER: str | None = os.environ.get("POSTGRES_SERVER")
POSTGRES_DB: str | None = os.environ.get("POSTGRES_DATABASE")
