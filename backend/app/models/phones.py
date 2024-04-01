from core.database import Base
from sqlalchemy import Column, Integer, String


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    value = Column(String(100))

    def __repr__(self):
        return f"Phone(id={self.id}, phone={self.value})"
