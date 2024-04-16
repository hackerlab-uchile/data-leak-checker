from models.password import Password
from sqlalchemy.orm import Session

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def add_or_create_all_passwords(
    db: Session, list_passwords: list[str]
) -> list[Password]:
    saved_passwords = []
    new_passwords: dict[str, int] = {}
    for p in list_passwords:
        instance = db.query(Password).filter_by(hash_password=p).one_or_none()
        if instance:
            # Add +1 to counter
            setattr(instance, "count", instance.count + 1)
        elif new_passwords.get(p):
            new_passwords[p] += 1
        else:
            new_passwords[p] = 1
    for value, total in new_passwords.items():
        instance = Password(hash_password=value, count=total)
        saved_passwords.append(instance)

    db.add_all(saved_passwords)
    db.commit()
    return saved_passwords


# def add_or_create_all_passwords(
#     db: Session, list_passwords: list[str]
# ) -> list[Password]:
#     saved_passwords = []
#     new_passwords: dict[str, int] = {}
#     for p in list_passwords:
#         instance = db.query(Password).filter_by(hash_password=p).one_or_none()
#         if instance:
#             # Add +1 to counter
#             setattr(instance, "count", instance.count + 1)
#         elif new_passwords.get(p):
#             new_passwords[p] += 1
#         else:
#             new_passwords[p] = 1
#             # instance = Password(hash_password=p, count=1)
#             # db.add(instance)
#             # saved_passwords.append(instance)
#     for value, total in new_passwords.items():
#         instance = Password(hash_password=value, count=total)
#         saved_passwords.append(instance)

#     db.add_all(saved_passwords)
#     db.commit()
#     return saved_passwords
