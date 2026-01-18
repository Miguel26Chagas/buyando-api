import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL, echo = True)

AsyncSessionLocal = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
class Base(AsyncAttrs, DeclarativeBase):
    pass

