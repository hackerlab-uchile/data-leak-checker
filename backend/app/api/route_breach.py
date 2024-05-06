from hashlib import sha256
from typing import List

from core.database import get_db
from fastapi import APIRouter, Depends
from models.breach import Breach
from models.data_leak import DataLeak
from models.data_type import DataType
from repositories import breach_repository
from schemas.breaches import Breach as BreachSchema
from schemas.breaches import BreachCreate
from schemas.data_leak import DataLeakBase, DataLeakInput, DataLeakShow
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

router = APIRouter()


@router.post("/", response_model=BreachCreate)
def create_breach(breach: BreachCreate, db: Session = Depends(get_db)):
    new_breach = breach_repository.create_breach(db, breach)
    return new_breach


@router.post("/deprecated/data/", response_model=List[BreachSchema])
def get_breachdata_deprecated(data_leak: DataLeakBase, db: Session = Depends(get_db)):
    """Returns information about data breaches related to an email"""
    found_breaches = (
        db.query(Breach)
        .join(DataLeak)
        .filter(DataLeak.hash_value == data_leak.hash_value)
    ).all()
    return found_breaches


@router.post("/data/", response_model=List[DataLeakShow])
def get_breaches_info(payload: DataLeakInput, db: Session = Depends(get_db)):
    """Returns information about data breaches related to an email"""
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


@router.post("/data/demo/", response_model=List[DataLeakShow])
def get_breaches_demo(payload: DataLeakInput, db: Session = Depends(get_db)):
    """Returns information about data breaches related to an email"""
    # hash_value = sha256(payload.value.encode("UTF-8")).hexdigest()
    # dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
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
