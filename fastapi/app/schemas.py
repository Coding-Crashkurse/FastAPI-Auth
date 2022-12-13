from enum import Enum
from typing import Union

from pydantic import BaseModel, EmailStr


class Roles(Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserRegister(UserBase):
    password: str

class UserDB(UserBase):
    id: str
    role: Roles = "user"
    is_active: bool = False
    hashed_password: str
    
    class Config:
        orm_mode = True

class UserPlain(BaseModel):
    id: str
    username: str
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str