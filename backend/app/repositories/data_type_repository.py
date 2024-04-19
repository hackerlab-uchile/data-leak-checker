from models.breach_data import BreachData
from models.data_type import DataType
from sqlalchemy.orm import Session


def get_all_data_types() -> list[str]:
    return [dtype.value for dtype in list(DataType)]


def get_all_data_types_in_name_list(names: list[str]) -> list[str]:
    types_to_return: set = set()
    for name in names:
        types_to_return.add(DataType.from_str(name).value)
    return list(types_to_return)


def save_breach_data(db: Session, **kwargs):
    db_item = BreachData(**kwargs)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
