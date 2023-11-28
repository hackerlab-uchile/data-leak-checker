from core.database import get_db
from fastapi import APIRouter, Depends
from models.emails import Email
from pydantic import EmailStr
from repositories import breach_repository
from schemas.breaches import Breach, BreachCreate
from schemas.emails import Email as EmailSchema
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=BreachCreate)
def create_breach(breach: BreachCreate, db: Session = Depends(get_db)):
    new_breach = breach_repository.create_breach(db, breach)
    return new_breach

@router.get("/email/{email}", response_model=EmailSchema|None)
def get_breachdata_by_email(email: EmailStr, db: Session = Depends(get_db)):
    """Returns information about data breaches related to this email"""
    return db.query(Email).where(Email.email == email).one_or_none()