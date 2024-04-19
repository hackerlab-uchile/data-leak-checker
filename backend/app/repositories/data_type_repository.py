from models.breach_data import BreachData
from models.data_type import DataType
from sqlalchemy.orm import Session


def get_data_type_by_name(db: Session, name: str) -> DataType | None:
    item = db.query(DataType).filter(DataType.name == name).one_or_none()
    return item


def get_all_data_types(db: Session) -> list[DataType]:
    all_types = db.query(DataType).all()
    return all_types


def get_only_key_types(db: Session) -> list[DataType]:
    key_types = ["email", "phone", "rut"]
    all_key_types = db.query(DataType).filter(DataType.name.in_(key_types)).all()
    return all_key_types


def get_all_data_types_in_name_list(db: Session, names: list[str]) -> list[DataType]:
    items = db.query(DataType).filter(DataType.name.in_(names)).all()
    return items


def save_breach_data(db: Session, **kwargs):
    db_item = BreachData(**kwargs)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
