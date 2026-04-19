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

    async def update_user(self, data, user: User):
        user.name = data.name or user.name
        user.email = data.email or user.email

        try:
            await self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f'Erro Ao Salvar no banco de Dados: {e}')
            raise e
        return {'msg': 'Alteracao feita com sucesso!'}

            

    async def update_password_user(self, password, user: User) -> bool:
        user.password = password
        try:
            await self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f'Erro Ao Salvar no banco de Dados: {e}')
            return False
        return True

    async def delete_user(self):
        pass

    async def add_photo(self, secure_url, public_id, user: User):
        self.db

        user.profile_photo = secure_url
        user.public_photo_id = public_id

        try:
            await self.db.commit()
            # await self.db.refresh(user)
        except Exception as e :
            await self.db.rollback()
            print(f'Erro Ao Salvar no banco de Dados: {e}')
            raise e
                