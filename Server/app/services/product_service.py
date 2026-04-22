import asyncio
from fastapi import HTTPException, File, UploadFile, Depends
from app.models import Product, User, PhotosProduct
from app.repository import ProductRepo, SellerRepo, RefreshDataRepo
from app.cloudinary import add_any_photos_in_cloudinary
from app.dependencies import ProductForm
from app.schemas import ProductUpdateSchema

from typing import List
from uuid import UUID

class ProductService():
    def __init__(self, db, product_repo = ProductRepo,
                seller_repo = SellerRepo, refresh_datas_repo = RefreshDataRepo):
        self.db = db
        self.product_repo = product_repo(db)
        self.seller_repo = seller_repo(db)
        self.refresh_datas_repo = refresh_datas_repo(db)

    async def product(self, user: User, data: ProductForm = Depends(), files_urls: List[UploadFile] = File(...)):
        if not user.role == 'seller':
            raise HTTPException(
                status_code=403,
                detail='Você precisa criar sua conta vendedor pra vender produtos.'
            )
        
        is_seller = await self.seller_repo.check_user_is_seller(user)
        if not is_seller:
            raise HTTPException(status_code=403, detail='Usuario nao e vendedor')
        
        photos = []
        try:
            responses = await add_any_photos_in_cloudinary(files_urls)
            photos = [
                PhotosProduct(
                    photo_url = res['secure_url'],
                    public_photo_id=res['public_id']
                )
                for res in responses
            ]
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail = f'Por favor, insira uma imagem do seu produto, {e}'
            )
        
        try:
            product = await self.product_repo.create_product(data, is_seller, photos)
        except Exception as e:
            print(f'Erro ao Criar Produto: {e}')
            raise HTTPException(status_code=500, details = 'Erro ao Criar Produto')
        return product
    
    async def update_product(self, product_id:UUID, data: ProductUpdateSchema, user: User):
        if not user.role == 'seller':
            raise HTTPException(status_code=403, detail='Voce nao tem permissao pra isto')
        
        product = await self.product_repo.check_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Produto Nao encontrado')

        seller_of_product = await self.seller_repo.product_of_seller(product)
        if not seller_of_product.user_id == user.id:
            raise HTTPException(status_code=403, detail='Negado, voce nao pode alterar esse produto')

        update_data = data.model_dump(exclude_unset=True)
        for  key, value in update_data.items():
            setattr(product, key, value)
        try:
            await self.refresh_datas_repo(product)
        except Exception as e:
            print(f'Erro ao Atualizar: {e}')
            raise HTTPException(status_code=500, detail='Erro ao atualizar dados')
        return product

    async def delete_product(self, product_id:UUID, user: User):
        if not user.role == 'seller':
            raise HTTPException(status_code=403, detail='Voce nao tem permissao pra isto')
        
        seller = await self.seller_repo.check_user_is_seller(user)
        if not seller:
            raise HTTPException(status_code=400, detail='Vendedor nao encontrado')

        product  = await self.product_repo.seller_and_product(product_id, user)
        if not product:
            raise HTTPException(status_code=404,
                                detail='Produto nao encontrado ou nao pertencente a si')
        try:
            await self.product_repo.delete_product(product)
        except Exception as e:
            print(f'Erro ao deletar: {e}')
            raise HTTPException(status_code=500, detail=f'Erro ao deletar produto')
        return {'msg': 'Apagado com sucesso!'}

    async def all_products(self):
        products = await self.product_repo.list_all_products()
        if not products:
            raise HTTPException(status_code=404, detail='Nao ha produtos disponiveis')
        return products

    async def update_photos_product(self):
        pass