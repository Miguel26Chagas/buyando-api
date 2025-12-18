from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    name: str
    email: str
    number_phone: Optional[str] = None
    password: str
    active: Optional[bool] = True
    admin: Optional[bool] = False

    class config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class config:
        from_attributes = True