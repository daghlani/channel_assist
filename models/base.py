from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from config import database
from logger import logger

engine = create_engine(database.dbadress)
if not database_exists(engine.url):
    create_database(engine.url)
    logger.info('The database was built')
else:
    logger.debug('database exist')

engine = create_engine(database.dbadress)
Session = sessionmaker(bind=engine)

Base = declarative_base()

metadata = MetaData()

