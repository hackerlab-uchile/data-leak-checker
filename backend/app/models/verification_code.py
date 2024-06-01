from core.database import Base
from models.user import User
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

CODE_LENGTH = 6
CODE_EXPIRE_MINUTES = 5


class VerificationCode(Base):
    __tablename__ = "verification_code"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(length=CODE_LENGTH), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    used: Mapped[bool] = mapped_column(Boolean, server_default=false())

    user_owner: Mapped["User"] = relationship("User", foreign_keys=[user_id])

    @property
    def associated_value(self) -> str:
        if self.user_owner:
            return self.user_owner.value
        return ""

    @property
    def value_type(self) -> str:
        if self.user_owner:
            return self.user_owner.data_type.name
        return ""

    def __repr__(self):
        return f"VerificationCode(id={self.id}, code={self.code}, created_at={self.created_at}, user_owner={self.user_owner})"
