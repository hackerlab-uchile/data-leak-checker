import secrets
from datetime import timedelta

from models.user import User
from models.verification_code import CODE_EXPIRE_MINUTES, CODE_LENGTH, VerificationCode
from pydantic import PositiveInt
from schemas.verification_code import (
    VerificationCodeCreate,
    VerificationCodeInput,
    VerificationCodeShow,
)
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false


def generate_random_code() -> str:
    """Returns a random 6-digit sequence of numbers"""
    n = CODE_LENGTH
    output = ""
    for _ in range(n):
        output += str(secrets.choice(range(0, 10)))
    return output


def generate_new_verification_code(
    user_id: PositiveInt, db: Session
) -> VerificationCode:
    random_code: str = generate_random_code()
    new_code = VerificationCodeCreate(code=random_code, user_id=user_id)
    return save_verification_code(db=db, vcode=new_code)


def delete_expired_verification_codes(db: Session) -> None:
    expire_delta = timedelta(minutes=1)
    db.query(VerificationCode).filter(
        VerificationCode.created_at + expire_delta < func.now()
    ).delete()
    db.commit()


def get_valid_verification_code_by_value_and_data_type(
    db: Session, value: str, data_type_id: int
) -> VerificationCode | None:
    candidate = (
        db.query(VerificationCode)
        .join(User)
        .filter(User.value == value, User.data_type_id == data_type_id)
        .filter(
            VerificationCode.created_at + timedelta(minutes=CODE_EXPIRE_MINUTES)
            > func.now()
        )
        .order_by(desc(VerificationCode.created_at))
        .first()
    )
    if candidate:
        return candidate
    return None


def get_verification_code(
    vcode: VerificationCodeInput, db: Session
) -> VerificationCode | None:
    code = vcode.code
    associated_value = vcode.value
    result = (
        db.query(VerificationCode)
        .join(User, User.id == VerificationCode.user_id)
        .filter(
            VerificationCode.code == code,
            VerificationCode.used == false(),
            User.value == associated_value,
        )
        .first()
    )
    if result:
        return result
    return None


def save_verification_code(
    db: Session, vcode: VerificationCodeCreate
) -> VerificationCode:
    db_item = VerificationCode(**vcode.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_verification_code(db: Session, vcode: VerificationCode) -> None:
    db_item = vcode
    db.delete(db_item)
    db.commit()


def mark_verification_code_as_used(vcode: VerificationCode, db: Session) -> None:
    vcode.used = True
    db.commit()
