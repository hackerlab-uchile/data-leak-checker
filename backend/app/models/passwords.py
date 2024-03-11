from core.database import Base
from sqlalchemy import Column, Integer, String


class Password(Base):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True)
    hash_password = Column(String(40))

    def __repr__(self):
        return f"Password(id={self.id}, hash_password={self.hash_password})"