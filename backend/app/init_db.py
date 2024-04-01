from core.database import Base, engine, test_engine
from models.breach_data import BreachData
from models.breaches import Breach
from models.data_types import DataType
from models.email_leaks import EmailLeak
from models.emails import Email
from models.passwords import Password
from models.phone_leaks import PhoneLeak
from models.phones import Phone
from models.rut_leaks import RutLeak
from models.ruts import Rut
from sqlalchemy_utils import create_database, database_exists

if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(bind=engine)

if not database_exists(test_engine.url):
    create_database(test_engine.url)
Base.metadata.create_all(bind=test_engine)
