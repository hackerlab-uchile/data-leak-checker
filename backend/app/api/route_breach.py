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
    """Returns information about data breaches related to an email"""
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

@router.get("/rut/{rut}", response_model=List[BreachSchema])
def get_breachdata_by_rut(rut: str, db: Session = Depends(get_db)):
    """Returns information about data breaches related to a rut"""
    rut_dtype = db.query(DataType).where(DataType.dtype == "rut").one_or_none()
    if rut_dtype is None:
        return []
    data =  db.query(Data).where(and_(Data.type_id == rut_dtype.id, Data.value == rut)).one_or_none()
    if data is None:
        return []
    data_leaks = db.query(DataLeak).where(DataLeak.data_id == data.id).all()
    print("Data Leaks:", data_leaks)
    breaches = []
    for d in data_leaks:
        breaches.append(d.breach)
    return breaches

@router.get("/phone/{phone}", response_model=List[BreachSchema])
def get_breachdata_by_phone(phone: str, db: Session = Depends(get_db)):
    """Returns information about data breaches related to a phone"""
    phone_dtype = db.query(DataType).where(DataType.dtype == "phone").one_or_none()
    print(f"{phone_dtype=}")
    if phone_dtype is None:
        print("!!!!! No Phone Type :c")
        return []
    data =  db.query(Data).where(and_(Data.type_id == phone_dtype.id, Data.value == phone)).one_or_none()
    if data is None:
        print("!!!!! No Data with phone! :c")
        return []
    data_leaks = db.query(DataLeak).where(DataLeak.data_id == data.id).all()
    print("Data Leaks:", data_leaks)
    breaches = []
    for d in data_leaks:
        breaches.append(d.breach)
    return breaches