from pydantic import BaseModel, EmailStr, Field, computed_field
from typing import Optional
from app.models.user import UserRole

from app.cloudinary import transform_cloudinary_url


from uuid import UUID

class UserMe(BaseModel):
    id: UUID 
    name: str 
    email: str
    public_photo_id: str | None

    @computed_field    
    @property
    def profile_photo(self) -> str | None:
        if not self.public_photo_id:
            return 'No Profile Photo'
        return transform_cloudinary_url(self.public_photo_id, profile='thumbnail')

    role: Optional[UserRole] | str
    activate: bool

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

