from enum import Enum

from pydantic import BaseModel, EmailStr


class Roles(Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = False
    role: Roles = "user"

class UserRegister(UserBase):
    password: str

class UserDB(UserBase):
    id: str
    hashed_password: str
    
    class Config:
        orm_mode = True