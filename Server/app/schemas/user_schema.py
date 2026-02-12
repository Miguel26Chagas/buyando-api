from pydantic import BaseModel, EmailStr, Field
from typing import Optional
class UserResponse(BaseModel):
    name: str
    email: EmailStr
    class Config:
        from_attributes = True
class UserUpdate(BaseModel):
    name: Optional[str] = None 
    email: Optional[EmailStr] = None
    class Config:
        from_attributes = True
class PasswordSchema(BaseModel):
    password: str = Field(min_length=8, 
                          description='Senha tem de conter no minimo 8 caractere')
    new_password:str
    class Config:
        from_attributes = True

