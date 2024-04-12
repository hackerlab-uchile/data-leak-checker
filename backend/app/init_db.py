from core.database import Base, engine, test_engine
from models.breach_data import BreachData
from models.breaches import Breach
from models.data_leaks import DataLeak
from models.data_types import DataType
from sqlalchemy_utils import create_database, database_exists

if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(bind=engine)

if not database_exists(test_engine.url):
    create_database(test_engine.url)
Base.metadata.create_all(bind=test_engine)
