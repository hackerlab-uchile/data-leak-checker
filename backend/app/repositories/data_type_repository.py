from models.breach_data import BreachData
from models.data_types import DataType
from schemas.breach_data import BreachDataCreate as BreachDataCreateSchema
from sqlalchemy.orm import Session


def get_data_type_by_name(db: Session, name: str) -> DataType | None:
    item = db.query(DataType).filter(DataType.dtype == name).one_or_none()
    return item


def save_breach_data(db: Session, **kwargs):
    db_item = BreachData(**kwargs)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
