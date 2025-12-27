from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    name: str
    price: float
    qtd: Optional[int] = 0
    category: str
    detail: Optional[str]
    disponible: Optional[bool] = True

    class Config:
        from_attributes = True

class ProductUpadate(BaseModel):
    name: Optional[str] = None
    seller: Optional[int] = None
    price: Optional[float] = None
    qtd: Optional[str] = None
    category: Optional[str] = None
    disponible: Optional[bool] = None

    class Config:
        from_attributes = True
