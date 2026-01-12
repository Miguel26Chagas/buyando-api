from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ItemOrderSchema(BaseModel):
    order_id: UUID
    qtd_item: UUID

    class Config:
        from_attributes = True