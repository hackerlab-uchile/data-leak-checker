from typing import List

from core.database import get_db
from fastapi import APIRouter, Depends
from models.data import Data
from models.data_leaks import DataLeak
from models.data_types import DataType
from pydantic import EmailStr
from repositories import breach_repository
from schemas.breaches import Breach as BreachSchema
from schemas.breaches import BreachCreate
from sqlalchemy import and_
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=BreachCreate)
def create_breach(breach: BreachCreate, db: Session = Depends(get_db)):
    new_breach = breach_repository.create_breach(db, breach)
    return new_breach

@router.get("/email/{email}", response_model=List[BreachSchema])
def get_breachdata_by_email(email: EmailStr, db: Session = Depends(get_db)):
    """Returns information about data breaches related to this email"""
    email_dtype = db.query(DataType).where(DataType.dtype == "email").one_or_none()
    if email_dtype is None:
        return []
    data =  db.query(Data).where(and_(Data.type_id == email_dtype.id, Data.value == email)).one_or_none()
    if data is None:
        return []
    data_leaks = db.query(DataLeak).where(DataLeak.data_id == data.id).all()
    print("Data Leaks:", data_leaks)
    breaches = []
    for d in data_leaks:
        breaches.append(d.breach)
    return breaches