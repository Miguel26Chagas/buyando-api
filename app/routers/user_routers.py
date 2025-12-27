from fastapi import Depends, HTTPException, APIRouter
from app.dependencies import verify_token
from app.models import User
from app.schemas import PasswordSchema, UserUpdate
from app.security import verify_password, hash_password
from app.db.database import get_db

from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/user',
    tags=['user'],
    dependencies=[Depends(verify_token)]
)

@router.patch('/update/password')
async def update_password(data:PasswordSchema, user: User = Depends(verify_token), db: Session = Depends(get_db)):
    password = verify_password(data.password, user.password)

    if not password:
        raise HTTPException(
            status_code=400,
            detail='Senha Incorreta'
        )
    user.password = hash_password(data.new_password)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao salvar no Banco de Dados, {e}'
        )
    return {'msg': 'Senha alterada com sucesso!'}

@router.patch('/update/data')
async def update_data(data: UserUpdate, user: User = Depends(verify_token), db: Session = Depends(get_db)):

    if not data.name == None or '':
        user.name = data.name
    elif not data.email == None or '':
        user.email = data.email
    else:
        raise HTTPException(status_code=400, detail='Nada aqui pra salvar')
        
    

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(
            status_code = 500,
            detail = f'Erro ao atualizar dados!, {e}'
        )
    return {'msg': 'Ação concluida!'}

