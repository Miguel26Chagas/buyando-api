from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Seller, Product, UserRole

from uuid import UUID

class SellerRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_seller(self, data, user: User):
        seller_active = Seller(
            seller_name = data.seller_name,
            locate = data.locate,
            user_id = user.id,
            number_phone = data.number_phone,
            email_seller = data.email_seller,
            description = data.description
        )
        user.role = UserRole.SELLER
        try:
            self.db.add(seller_active)
            await self.db.commit()
            await self.db.refresh(seller_active)
        except Exception as e:
            print('Erro ao Salvar no banco de dados')
            raise e
        return print('SAVED')

    async def check_seller(self, seller_id: UUID):
        stmt = select(Seller).where(Seller.id == seller_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
    
    async def product_of_seller(self, product: Product):
        stmt = select(Seller).where(Seller.id == product.seller_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
    
    async def check_user_is_seller(self, user: User):
        stmt = select(Seller).where(Seller.user_id == user.id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
    
    async def list_products(self, user: User):
        stmt = select(Seller).where(Seller.user_id == user.id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

