from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

from uuid import UUID
from typing import List

class UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_email_or_name(self, email: str, name: str) -> bool:
        stmt = select(User).where(or_(User.email == email, User.name == name))
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none() is not None
    
    async def username_exist(self, username) -> User:
        stmt = select(User).where(or_(User.email == username, User.name == username))
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        try:    
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
        except Exception as e:
            await self.db.rollback()
            print(f'DEBUG ERROR:{e}')
            raise e
        return user
    
    async def get_user(self, user_id:UUID) -> User:
        stmt = select(User).where(User.id == user_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def update_user(self):
        pass

    async def delete_user(self):
        pass