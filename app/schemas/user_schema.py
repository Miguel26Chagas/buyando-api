from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email:str
    password: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email_or_name: str
    password: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None 
    email: Optional[str] = None

    class Config:
        from_attributes = True



class PasswordSchema(BaseModel):
    password:str
    new_password:str

    class Config:
        from_attributes = True

