import random
from hashlib import sha256
from typing import List

from core.database import get_db
from fastapi import APIRouter, Depends
from models.breach import Breach
from models.breach_data import BreachData
from models.data_leak import DataLeak
from models.data_type import DataType
from schemas.data_leak import DataLeakInput, DataLeakShow
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

router = APIRouter()


@router.post("/data/", response_model=List[DataLeakShow])
def get_breaches_info(payload: DataLeakInput, db: Session = Depends(get_db)):
    """Returns information about data breaches related to a value and type"""
    hash_value = sha256(payload.value.encode("UTF-8")).hexdigest()
    dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
    if dtype is None:
        # TODO: Throw error
        # TODO: Se puede hacer una dependency, que entregue el dtype correspondiente
        # TODO: Cómo se hacía una dependecy? xd
        return []
    found_breaches = (
        db.query(DataLeak)
        .join(Breach, Breach.id == DataLeak.breach_id)
        .filter(DataLeak.hash_value == hash_value)
        .filter(DataLeak.data_type_id == dtype.id)
        .order_by(desc(Breach.breach_date))
    ).all()
    return found_breaches


# @router.post("/data/demo/", response_model=List[DataLeakShow])
def get_breaches_demo(payload: DataLeakInput, db: Session = Depends(get_db)):
    """Returns information about random data breaches. For demo purposes"""
    if payload.dtype == "email" and not looks_like_email(payload.value):
        return []
    elif payload.dtype == "rut" and not payload.value.isnumeric():
        return []
    rand_dl = (
        db.query(DataLeak)
        .join(DataType)
        .filter(DataType.name == payload.dtype)
        .order_by(func.random())
        .first()
    )
    if rand_dl is None or payload.dtype == "phone":
        # Por fines de demostración, consultar por teléfonos no entregará filtración
        return []
    found_breaches = (
        db.query(DataLeak)
        .join(Breach, Breach.id == DataLeak.breach_id)
        .filter(DataLeak.hash_value == rand_dl.hash_value)
        .filter(DataLeak.data_type_id == rand_dl.data_type_id)
        .order_by(desc(Breach.breach_date))
    ).all()
    return found_breaches


@router.post("/data/demo/", response_model=List[DataLeakShow])
def get_breaches_demo2(payload: DataLeakInput, db: Session = Depends(get_db)):
    """Returns information about random data breaches. For demo purposes"""
    dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
    if payload.dtype == "email" and not looks_like_email(payload.value):
        return []
    elif payload.dtype == "rut" and not payload.value.isnumeric():
        return []
    elif dtype is None:
        return []

    n_limit = random.randint(2, 5)
    rand_breaches = (
        db.query(Breach)
        .join(BreachData)
        .filter(BreachData.data_type_id == dtype.id)
        .order_by(func.random())
        .limit(n_limit)
        .all()
    )
    if len(rand_breaches) == 0 or payload.dtype == "phone":
        # Por fines de demostración, consultar por teléfonos no entregará filtración
        return []
    rand_breaches.sort(key=lambda x: str(x.breach_date), reverse=True)
    found_breaches: List[DataLeak] = []
    for breach in rand_breaches:
        dl = DataLeak()
        dl.data_type = dtype
        dl.breach_found = breach
        n_found = len(breach.data_breached)
        roll = random.randint(max(0, n_found - 2), n_found)
        picks = random.sample(breach.data_breached, k=roll)
        found_with = set([dtype, *picks])
        dl.found_with = list(found_with)
        found_breaches.append(dl)

    return found_breaches


def looks_like_email(value: str) -> bool:
    # NO se usa regex, porque no es necesario para una simple demo
    dot_splitted = value.split(".")
    arroba_splitted = value.split("@")
    result = (
        len(arroba_splitted) == 2
        and len(dot_splitted) > 1
        and len(dot_splitted[-1]) > 1
    )
    return result
