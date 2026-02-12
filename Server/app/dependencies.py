from fastapi import HTTPException, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.security import oauth2_schema

from pydantic import EmailStr
from typing import Optional


import jwt
from app.security import SECRET_KEYS, ALG
from app.models import User

async def verify_token(token: str = Depends(oauth2_schema), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEYS, ALG)
        user_id = payload.get('sub')
    except jwt.DecodeError as e:
        raise HTTPException(
            status_code=401,
            detail=f'Acesso negado, verifique a data do token, {e}'
        )
    stmt = select(User).where(User.id == user_id)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user

class UserForm():
    def __init__(self,
                 name: str = Form(...),
                 email: EmailStr = Form(...),
                 password: str = Form(min_length=8,
                                      description='Senha tem de conter no minimo 8 caractere'),):
        self.name = name
        self.email = email
        self.password = password

class ProductForm():
    def __init__(self, 
                 name: str = Form(...),
                 price: float = Form(...),
                 qtd_stock: Optional[int] = Form(default=0),
                 category: str = Form(...),
                 detail: Optional[str] = Form(...),
                 disponible: Optional[bool] = Form(default=True)):
        
        self.name = name
        self.price = price
        self.qtd = qtd_stock
        self.category = category
        self.detail = detail
        self.disponible = disponible
        
