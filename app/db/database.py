import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL, echo = True)

AsyncSessionLocal = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=True,
    class_=True,
    bind=engine
)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
class Base(AsyncAttrs, DeclarativeBase):
    pass

