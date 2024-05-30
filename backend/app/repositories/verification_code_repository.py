import random
from datetime import timedelta
from typing import Literal

from models.verification_code import VerificationCode
from repositories.data_type_repository import get_data_type_by_name
from schemas.verification_code import VerificationCodeCreate, VerificationCodeShow
from sqlalchemy import func
from sqlalchemy.orm import Session


def generate_random_code() -> int:
    return random.randrange(100_000, 1_000_000)


def generate_new_verification_code(
    value: str, dtype_name: Literal["email", "phone"], db: Session
) -> VerificationCode:
    random_code = generate_random_code()
    dtype = get_data_type_by_name(db=db, name=dtype_name)
    if dtype is None:
        raise Exception(f"No existe DataType con name={dtype_name}")
    old_code = get_verification_code_by_value_and_data_type(db, value, dtype.id)
    if old_code:
        delete_verification_code(db, old_code)
    new_code = VerificationCodeCreate(
        code=random_code, associated_value=value, data_type_id=dtype.id
    )
    return save_verification_code(db=db, vcode=new_code)


def delete_expired_verification_codes(db: Session) -> None:
    expire_delta = timedelta(minutes=1)
    db.query(VerificationCode).filter(
        VerificationCode.created_at + expire_delta < func.now()
    ).delete()
    db.commit()


def get_verification_code_by_value_and_data_type(
    db: Session, value: str, data_type_id: int
) -> VerificationCode | None:
    return (
        db.query(VerificationCode)
        .filter(
            VerificationCode.associated_value == value,
            VerificationCode.data_type_id == data_type_id,
        )
        .first()
    )


def get_verification_code(
    vcode: VerificationCodeShow, db: Session
) -> VerificationCode | None:
    code = vcode.code
    associated_value = vcode.associated_value
    result = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.code == code,
            VerificationCode.associated_value == associated_value,
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
