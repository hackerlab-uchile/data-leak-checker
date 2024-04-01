from typing import List

from core.database import get_db
from fastapi import APIRouter, Depends
from models.breaches import Breach
from models.email_leaks import EmailLeak
from models.emails import Email
from models.phone_leaks import PhoneLeak
from models.phones import Phone
from models.rut_leaks import RutLeak
from models.ruts import Rut
from pydantic import EmailStr
from repositories import breach_repository
from schemas.breaches import Breach as BreachSchema
from schemas.breaches import BreachCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=BreachCreate)
def create_breach(breach: BreachCreate, db: Session = Depends(get_db)):
    new_breach = breach_repository.create_breach(db, breach)
    return new_breach


@router.get("/email/{email}", response_model=List[BreachSchema])
def get_breachdata_by_email(email: EmailStr, db: Session = Depends(get_db)):
    """Returns information about data breaches related to an email"""
    found_breaches = (
        db.query(Breach).join(EmailLeak).join(Email).filter(Email.value == email)
    ).all()
    return found_breaches


@router.get("/rut/{rut}", response_model=List[BreachSchema])
def get_breachdata_by_rut(rut: str, db: Session = Depends(get_db)):
    """Returns information about data breaches related to a rut"""
    found_breaches = (
        db.query(Breach).join(RutLeak).join(Rut).filter(Rut.value == rut)
    ).all()
    return found_breaches


@router.get("/phone/{phone}", response_model=List[BreachSchema])
def get_breachdata_by_phone(phone: str, db: Session = Depends(get_db)):
    """Returns information about data breaches related to a phone"""
    found_breaches = (
        db.query(Breach).join(PhoneLeak).join(Phone).filter(Phone.value == phone)
    ).all()
    return found_breaches
