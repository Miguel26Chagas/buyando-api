from __future__ import annotations
from pydantic import BaseModel, fields, computed_field
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID

from app.schemas import SellerResponseBase

from app.cloudinary import transform_cloudinary_url
class ProductResponse(BaseModel):
    id: UUID
    name: str
    price: float
    qtd_stock: int
    category: str
    seller_id: UUID
    detail: Optional[str]
    disponible: Optional[bool] = True
    seller: SellerResponseBase
    photo_urls: Optional[List['PhotosProductResponse']]
    class Config:
        from_attributes = True
class PhotosProductResponse(BaseModel):
    public_photo_id: str

    @computed_field
    @property

    def photo_url(self) -> str:
        return transform_cloudinary_url(self.public_photo_id, profile='order_list')

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    qtd_stock: Optional[int] = None
    detail: Optional[str] = None
    disponible: Optional[bool] = None

    class Config:
        from_attributes = True
