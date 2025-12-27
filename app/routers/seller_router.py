from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.models import User, Seller
from app.schemas import UserSchema, SellerSchema
from app.security import hash_password, verify_password, create_token, oaut2_form
from app.dependencies import verify_token
from app.db.database import get_db

router = APIRouter(
    prefix='/seller',
    tags=['seller'],
    dependencies=[Depends(verify_token)]
)

@router.post('/active')
async def seller_active(data: SellerSchema, user: User = Depends(verify_token), db: Session = Depends(get_db)):
    stmt = select(Seller).where(Seller.user_id == user.id)
    seller_exist = db.execute(stmt).scalar_one_or_none()

    if seller_exist:
        raise HTTPException(
            status_code=400,
            detail='Este usuario ja tem ativo uma conta vendedor'
        )
    if data.email_seller == None or '':
        data.email_seller = user.email

    seller_active = Seller(
        seller_name = data.seller_name,
        locate = data.locate,
        user_id = user.id,
        number_phone = data.number_phone,
        email_seller = data.email_seller,
        description = data.description
    )

    user.role = 'SELLER'

    try:
        db.add(seller_active)
        db.commit()
        db.refresh(seller_active)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail = 'Ocorreu um erro ao salvar no banco de dados'
        )
    return {'msg': f'Conta Vendedor Ativo!'}