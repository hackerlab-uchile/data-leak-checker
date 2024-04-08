from hashlib import sha256
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
from repositories import breach_repository
from schemas.breaches import Breach as BreachSchema
from schemas.breaches import BreachCreate
from schemas.emails import EmailBase
from schemas.phones import PhoneBase
from schemas.ruts import RutBase
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=BreachCreate)
def create_breach(breach: BreachCreate, db: Session = Depends(get_db)):
    new_breach = breach_repository.create_breach(db, breach)
    return new_breach


@router.post("/email/", response_model=List[BreachSchema])
def get_breachdata_by_email(email: EmailBase, db: Session = Depends(get_db)):
    """Returns information about data breaches related to an email"""
    found_breaches = (
        db.query(Breach).join(EmailLeak).join(Email).filter(Email.value == email.value)
    ).all()
    return found_breaches


@router.post("/rut/", response_model=List[BreachSchema])
def get_breachdata_by_rut(rut: RutBase, db: Session = Depends(get_db)):
    """Returns information about data breaches related to a rut"""
    found_breaches = (
        db.query(Breach).join(RutLeak).join(Rut).filter(Rut.value == rut.value)
    ).all()
    return found_breaches


@router.post("/phone/", response_model=List[BreachSchema])
def get_breachdata_by_phone(phone: PhoneBase, db: Session = Depends(get_db)):
    """Returns information about data breaches related to a phone"""
    found_breaches = (
        db.query(Breach).join(PhoneLeak).join(Phone).filter(Phone.value == phone.value)
    ).all()
    return found_breaches
