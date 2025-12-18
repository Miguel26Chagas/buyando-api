import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Session = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass



