from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_db
from app.security import oauth2_schema


import jwt
from app.security import SECRET_KEYS, ALG
from app.models import User

def verify_token(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEYS, ALG)
        user_id = payload.get('sub')
    except jwt.DecodeError as e:
        raise HTTPException(
            status_code=401,
            detail=f'Acesso negado, verifique a data do token, {e}'
        )
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one()

    return user