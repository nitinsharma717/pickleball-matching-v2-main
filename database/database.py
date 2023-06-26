from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import urllib.parse

server = 'nitintest.mysql.database.azure.com'
database = 'pickleball'
username = 'Andy1234'
password = 'Wipro@123'

# URL-encode the password
encoded_password = urllib.parse.quote_plus(password)

# Create the connection string
DATABASE_URL = f"mysql+pymysql://{username}:{encoded_password}@{server}/{database}"


db_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()

def get_db():
    """
    Function to generate db session
    :return: Session
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
 
