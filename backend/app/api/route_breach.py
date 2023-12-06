from typing import List

from core.database import get_db
from fastapi import APIRouter, Depends
from models.emails import Email
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
    """Returns information about data breaches related to this email"""
    emails =  db.query(Email).where(Email.email == email).all()
    print("Breacheeeees:", emails)
    breaches = []
    for e in emails:
        breaches.append(e.breach)
    return breaches