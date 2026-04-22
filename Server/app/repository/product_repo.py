from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Product, Seller

from uuid import UUID

class ProductRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, data, is_seller, photos):
        product = Product(
            name = data.name,
            seller_id = is_seller.id,
            price = data.price,
            qtd_stock = data.qtd,
            detail = data.detail,
            category = data.category,
            disponible = data.disponible,
            photo_urls = photos
        )
        try:
            self.db.add(product)
            await self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f'Erro ao salvar no Banco de Dados: {e}')
            raise e
        return product
        
    async def delete_product(self, product: Product):
        try:
            await self.db.delete(product)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e
        return print('DELECTED')
    
    async def list_products(self, seller_id: UUID):
        stmt = select(Product.id).where(Product.seller_id == seller_id)
        res = await self.db.execute(stmt)
        return res.scalar().all()

    async def check_product(self, product_id: UUID):
        stmt = select(Product).where(Product.id == product_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
    
    async def seller_of_product(self, seller_id: UUID): 
        stmt = select(Product.id).where(Product.seller_id == seller_id).limit(1)
        res = await self.db.execute(stmt)
        return res.scalar() is not None

    async def check_one_product(self, product_id:UUID):
        stmt = select(Product).filter(Product.id == product_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def product_to_proccessing(self, item: Product):
        stmt2 = select(Product).where(Product.id == item.product_id).with_for_update()
        res2 = await self.db.execute(stmt2)
        return res2.scalar_one_or_none()
    
    async def seller_and_product(self, product_id: UUID, seller:Seller):
        stmt = select(Product).where(and_(Product.id == product_id, Product.seller_id == seller.id))
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
    
    async def list_all_products(self, ):
        stmt = select(Product).options(selectinload(Product.photo_urls,),
                                   joinedload(Product.seller))
        res = await self.db.execute(stmt)
        return res.scalars().all()