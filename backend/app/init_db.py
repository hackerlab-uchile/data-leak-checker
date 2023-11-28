from core.database import Base, engine
from models.breaches import Breach
from models.emails import Email

# Inits database
Base.metadata.create_all(bind=engine)