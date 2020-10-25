# coding=utf-8

# 1 - imports
from datetime import date

from base import Session, engine, Base
from recordTypes import Dashboard_DAQ

# Inserts record in the database, requires database to be created
def insertRecord(location, dashboardName, sensorType, value):
	# 2 - generate database schema
	Base.metadata.create_all(engine)

	# 3 - create a new session
	session = Session()

	data = Dashboard_DAQ(None, location, dashboardName, sensorType, value)

	session.add(data)

	# 10 - commit and close session
	session.commit()
	session.close()
