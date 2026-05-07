from fastapi import HTTPException, File, UploadFile, Depends
from app.repository import SellerRepo, ProductRepo
from app.models import User
from app.schemas import SellerSchema

from uuid import UUID

class SellerService():
    def __init__(self, db, seller_repo = SellerRepo, product_repo = ProductRepo):
        self.seller_repo = seller_repo(db)
        self.product_repo = product_repo(db)

    async def seller_active(self, user: User, data: SellerSchema):
        seller = await self.seller_repo.check_user_is_seller(user)
        if seller:
            raise HTTPException(
                status_code=400,
                detail='Este usuario ja tem ativo uma conta vendedor'
            )
        if data.email_seller == None or '':
            data.email_seller = user.email
        try:
            seller = await self.seller_repo.create_seller(data, user)
        except Exception as e:
            print(f'Erro ao Salvar: {e}')
            raise HTTPException(status_code=500, detail= 'Erro ao Ativar conta vendedor')
        return seller

    async def seller_products(self, user: User, seller_id: UUID):
        if not user.role == 'seller':
            raise HTTPException(status_code=400, detail='Voce Nao vende nada')
       
        seller = await self.seller_repo.check_user_is_seller(user)
        if not seller:
            raise HTTPException(status_code=403, detail='Usuario nao e vendedor')
        
        products = await self.product_repo.list_products(seller_id)
        if not products:
            raise HTTPException(status_code=403, detail='Sem produtos a venda')
        return products
