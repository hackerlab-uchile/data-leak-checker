from typing import List

from core.database import get_db
from fastapi import APIRouter, Depends
from models.breach import Breach
from models.data_leak import DataLeak
from repositories import breach_repository
from schemas.breaches import Breach as BreachSchema
from schemas.breaches import BreachCreate
from schemas.data_leak import DataLeakBase
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=BreachCreate)
def create_breach(breach: BreachCreate, db: Session = Depends(get_db)):
    new_breach = breach_repository.create_breach(db, breach)
    return new_breach


@router.post("/data/", response_model=List[BreachSchema])
def get_breachdata(data_leak: DataLeakBase, db: Session = Depends(get_db)):
    """Returns information about data breaches related to an email"""
    found_breaches = (
        db.query(Breach)
        .join(DataLeak)
        .filter(DataLeak.hash_value == data_leak.hash_value)
    ).all()
    return found_breaches
