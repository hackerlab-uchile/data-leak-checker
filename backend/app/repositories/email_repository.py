from typing import Any, TypeVar

from core.database import Base
from models.emails import Email
from sqlalchemy.orm import Session

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

T = TypeVar("T", bound=Any)


def get_or_create(db: Session, model: T, **kwargs) -> T:
    instance = db.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        return instance
