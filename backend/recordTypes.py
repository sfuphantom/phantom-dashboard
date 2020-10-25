from sqlalchemy import Column, String, Integer, Date, PickleType, Text, cast, DateTime
from sqlalchemy.dialects.postgresql import ARRAY, array, JSONB, TIMESTAMP

from base import Base
import datetime

class Dashboard_DAQ(Base):
    """
    ipAddr: String (Primary Key), IP Address of eWEB site
    partnerName: String, Name of Partner where site is
    totalIterations: Integer, How many iterations Model will run through
    taggedObjects: JSON (Object Name: Label), User-labelled objects
    untaggedObjects: Array of Strings, All objects from site
    model: Pickle of autoTaggingModel Class
    predicted: JSON (Object Name: Predicted Label)
    state: String, State of model
    labeledTokens: JSON (Token Name: Label)
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