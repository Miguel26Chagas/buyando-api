from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
class ProductResponse(BaseModel):
    name: str
    price: float
    qtd: int
    category: str
    detail: Optional[str]
    disponible: Optional[bool] = True

    class Config:
        from_attributes = True

class ProductUpadate(BaseModel):
    name: Optional[str] = None
    seller_id: Optional[UUID] = None
    price: Optional[float] = None
    qtd: Optional[str] = None
    category: Optional[str] = None
    disponible: Optional[bool] = None

    class Config:
        from_attributes = True
