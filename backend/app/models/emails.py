from core.database import Base
from sqlalchemy import Column, Integer, String


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    value = Column(String(100), unique=True)

    def __repr__(self):
        return f"Email(id={self.id}, email={self.value})"
