from core.database import Base
from sqlalchemy import CHAR, Column, Integer


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    value = Column(CHAR(64))

    def __repr__(self):
        return f"Phone(id={self.id}, phone={self.value})"
