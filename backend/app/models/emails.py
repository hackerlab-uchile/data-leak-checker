from core.database import Base
from sqlalchemy import CHAR, Column, Integer


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    value = Column(CHAR(64), unique=True)  # hash

    def __repr__(self):
        return f"Email(id={self.id}, email={self.value})"
