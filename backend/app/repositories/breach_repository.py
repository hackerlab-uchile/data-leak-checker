from models.breaches import Breach
from schemas.breaches import BreachCreate as BreachCreateSchema
from sqlalchemy.orm import Session

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

def create_breach(db: Session, breach: BreachCreateSchema):
    db_item = Breach(**breach.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
