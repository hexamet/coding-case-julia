
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_model import Base
from sqlalchemy.orm import Session
import os
import time
from database_model import City
from api_logging import logger

DB_USER = os.getenv("MYSQL_USER","")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD","")
DB_NAME = os.getenv("MYSQL_DB","")

#dialect+connection://user:password@host:port/database_name
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@database:3306/{DB_NAME}"

engine = create_engine(DATABASE_URL)

#wait for database
for _ in range(10):
    try:
        time.sleep(5)
        connection = engine.connect()
    except Exception as e:
        logger.warning(e)
        logger.info("Retrying")
        
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_session():
    session = session_local()
    try:
        yield session
    finally:
        session.close()
        
def add_city_to_database(city:City, session:Session):
    
    if entry_exists(city, session):
        logger.info(f"City '{city.city}' already exists")
        return
        
    session.add(city)
    session.commit()
    session.refresh(city)
    
def entry_exists(city:City, session:Session)-> bool:
    if session.query(City).filter(City.id == city.id).first():
        return True
    return False
    
