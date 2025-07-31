
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_model import Base
import os
import time

DB_USER = os.getenv("MYSQL_USER","")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD","")
DB_NAME = os.getenv("MYSQL_DB","")

#dialect+connection://user:password@host:port/database_name
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@database:3306/{DB_NAME}"

engine = create_engine(DATABASE_URL)

#wait for database
for _ in range(10):
    try:
        connection = engine.connect()
    except Exception as e:
        print(e)
        print("Retying")
        time.sleep(3)
        
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_database():
    database = session_local()
    try:
        yield database
    finally:
        database.close()
