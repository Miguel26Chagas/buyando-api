from pydantic import BaseModel
from typing import Optional

class SellerSchema(BaseModel):
    seller_name: str
    locate: str
    number_phone: str
    email_seller: Optional[str] = None
    description: str 