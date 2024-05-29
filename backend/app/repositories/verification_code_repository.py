from models.verification_code import VerificationCode
from schemas.verification_code import VerificationCodeCreate, VerificationCodeShow
from sqlalchemy.orm import Session


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
