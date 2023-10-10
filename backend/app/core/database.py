from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_DB

DATABASE_URL = f"postgresql+psycopg3://{POSTGRES_DB}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoFlush=False, expire_on_commit=False, bind=engine
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass
