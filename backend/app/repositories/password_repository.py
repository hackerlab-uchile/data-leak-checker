from models.passwords import Password
from sqlalchemy.orm import Session

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def add_or_create_all_passwords(
    db: Session, list_passwords: list[str]
) -> list[Password]:
    saved_passwords = []
    for p in list_passwords:
        instance = db.query(Password).filter_by(hash_password=p).one_or_none()
        if instance:
            # Add +1 to counter
            setattr(instance, "count", instance.count + 1)
        else:
            instance = Password(hash_password=p, count=1)
            db.add(instance)
        saved_passwords.append(instance)
    db.commit()
    return saved_passwords
