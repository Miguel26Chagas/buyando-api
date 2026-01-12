from pydantic import BaseModel, EmailStr
from typing import Optional

from pydantic_extra_types.phone_numbers import PhoneNumber

class SellerSchema(BaseModel):
    seller_name: str
    locate: str
    number_phone: PhoneNumber
    email_seller: Optional[EmailStr] = None
    description: str 

    class Config:
        from_attributes = True