# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initializes connection with database, requires database to exist
engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')

Session = sessionmaker(bind=engine)

Base = declarative_base()