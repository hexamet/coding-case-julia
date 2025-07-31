from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class City(Base):
    __tablename__ = "city"

    id = Column(String, primary_key=True, index=True)
    city = Column(String)
    lat = Column(Float)
    lng = Column(Float)