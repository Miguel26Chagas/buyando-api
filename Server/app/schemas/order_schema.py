from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
class OrderResponse(BaseModel):
    id: UUID
    buyer_id: UUID
    seller_id: UUID
    status: str
    # each_price: float
    price_total: float
    list_product: List['ItemOrderResponse']
    class Config:
        from_attributes = True
class ItemOrderSchema(BaseModel):
    qtd_item: int
    class Config:
        from_attributes = True
class ItemOrderResponse(BaseModel):
    name_product: str
    qtd_item: int
    price: float
    class Config:
        from_attributes = True