from core.database import Base, engine
from models.breaches import Breach
from models.data import Data
from models.data_leaks import DataLeak
from models.data_types import DataType
from models.emails import Email
from models.passwords import Password

# Inits database
Base.metadata.create_all(bind=engine)