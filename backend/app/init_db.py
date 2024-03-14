from core.database import Base, engine, test_engine
from models.breaches import Breach
from models.data import Data
from models.data_leaks import DataLeak
from models.data_types import DataType
from models.emails import Email
from models.passwords import Password

# Inits database tables
Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=test_engine)
