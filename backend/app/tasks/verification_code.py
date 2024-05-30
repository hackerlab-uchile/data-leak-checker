from core.database import SessionLocal
from repositories.verification_code_repository import delete_expired_verification_codes


# TODO: Use as a repeating task
def remove_expired_verification_codes() -> None:
    print("Removing expired verification codes!")
    with SessionLocal() as db:
        delete_expired_verification_codes(db=db)
