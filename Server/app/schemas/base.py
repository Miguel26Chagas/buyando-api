from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from pydantic_extra_types.phone_numbers import PhoneNumber

class SellerResponseBase(BaseModel):
    seller_name: str
    number_phone: PhoneNumber
    
    class Config:
        from_attributes = True