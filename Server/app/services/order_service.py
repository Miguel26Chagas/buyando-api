from fastapi import HTTPException, UploadFile, File, BackgroundTasks
from app.models import Order, User, ItemOrder, StatusOrder
from app.repository import OrderRepo, ProductRepo, SellerRepo, RefreshDataRepo
from app.schemas import ItemOrderSchema
from uuid import UUID

class OrderService:
    def __init__ (self, db, order_repo = OrderRepo, seller_repo = SellerRepo,
                  product_repo = ProductRepo, refresh_data_repo = RefreshDataRepo):
        self.seller_repo = seller_repo(db)
        self.product_repo = product_repo(db)
        self.order_repo = order_repo(db)
        self.refresh_data_repo = refresh_data_repo(db)

    async def order(self, seller_id:UUID, user: User):        
        seller = await self.seller_repo.check_seller(seller_id)
        if not seller:
            raise HTTPException(status_code=403, detail='Este Usuario Nao é um Vendedor!')
            
        product = await self.product_repo.seller_of_product(seller_id)
        if not product:
            raise HTTPException(status_code=403, detail='Este vendedor não possui produtos.')
        
        order = await self.order_repo.exists_order(seller_id, user)
        if not order:
            try:
                order = await self.order_repo.create_order(seller_id, user)
            except Exception as e:
                print(f'Ocorreu algum erro ao fazer pedido: {e}')
                raise HTTPException(status_code=500, detail='Erro ao fazer um pedido!')
        return order

    async def add_item_order(self, product_id:UUID, data:ItemOrderSchema, user: User):
        product = await self.product_repo.check_one_product(product_id)
        if not product:
            raise HTTPException(status_code=400, detail='Este Produto Nao Foi encontrado')
        
        order = await self.order_repo.check_pendent_order(user, product)
        if not order:
            raise HTTPException(status_code=400, detail='Faca um pedido ao dono desse produto')
        
        if not order.buyer_id == user.id:
            raise HTTPException(status_code=403, detail='Este Pedido Nao e seu!')

        if data.qtd_item <= 0:
            raise HTTPException(status_code=400, detail='Por favor insira uma quantidade valida') 

        exist_item_order = await self.order_repo.exist_item_order(product_id, order)
        try:
            if exist_item_order:
                if product.qtd_stock < data.qtd_item:
                    raise HTTPException(status_code=400, detail="Estoque insuficiente")
                exist_item_order.qtd_item = data.qtd_item
                # exist_item_order.each_price = product.price
                exist_item_order.price = product.price * data.qtd_item
                order_item = exist_item_order
                order = await self.order_repo.update_item_order(order, order_item)
            else:
                if product.qtd_stock <= 0 or product.disponible != True:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Não ha {product.name} disponiveis no momento.'
                    )
                if product.qtd_stock < data.qtd_item:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Nao Ha essa quantidade no stock, só ha {product.qtd_stock}'
                    )
                order = await self.order_repo.add_item_order(order, product, data)
        except Exception as e:
            print(f'erro: {e}')
            raise HTTPException(status_code=500, detail='Ocorreu algum problema')
        return order

    async def checkout_order(self, order_id: UUID, user: User):
        order = await self.order_repo.checkout_order(order_id, user)
        if not order or not order.list_product:
            raise HTTPException(status_code=400, detail='Compra Nao existente ou Sem produtos na compra')

        products = order.list_product
        try:
            for item in products:
                product = await self.product_repo.product_to_proccessing(item)
                if not product or product.disponible == False:
                    raise HTTPException(status_code=400, detail=f'Infelizmente nao ha mais {item.name_product} produto no stock')
                if product.qtd_stock < item.qtd_item:
                    raise HTTPException(status_code=400, detail=f'Lamento, so restam {product.qtd_stock} no stock.')
                product.qtd_stock -= item.qtd_item
            order.status = StatusOrder.AWAITING_PAYMENT
            await self.refresh_data_repo.refresh_order(order)
        except Exception as e:
            print(f"ERRO CRÍTICO: {e}")
            raise HTTPException(status_code=500, detail='Erro na operacao')
        return order
    
    async def list_orders(self, user):
        orders =  await self.order_repo.get_orders(user)
        if not orders:
            raise HTTPException(status_code=400, detail='Sem Pedidos ou compras')
        return orders

    async def confirm_payment(self, order_id: UUID):
        order = await self.order_repo.check_status_payment(order_id)
        if not order or not order.status == 'AWAITING_PAYMENT':
            raise HTTPException(status_code=400, detail='Nao ha compra a ser pago!')