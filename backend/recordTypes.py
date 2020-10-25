from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from base import Base
import datetime

class Dashboard_DAQ(Base):
    """
    This class defines the schema of the record that is stored in the database

    id: Integer (Primary Key), Incremented index (auto-generated)
    sampleTime: DateTime, timestamp of sensor reading
    location: String, where car was run
    dashboardName: String, which raspberry pi was used
    sensorType: String, Type of sensor
    value: JSONB, data collected from sensor, JSONB allows you
    to use column for different data formats
    """
    __tablename__ = 'Dashboard_DAQ'

    id=Column(Integer, primary_key=True)
    sampleTime=Column('sampleTime', DateTime, default=datetime.datetime.utcnow)
    location=Column('location', String(50))
    dashboardName=Column('dashboardName', String(50))
    sensorType=Column('sensorType', String(50))
    value=Column('value', JSONB)


    def __init__(self, sampleTime, location, dashboardName, sensorType, value):
        self.sampleTime = sampleTime
        self.location = location
        self.dashboardName = dashboardName
        self.sensorType = sensorType
        self.value = value