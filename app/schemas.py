from enum import Enum

from pydantic import BaseModel, EmailStr


class Roles(Enum):
    user = "user"
    admin = "admin"


class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
    is_active: bool = False
    role: Roles = "user"

    class Config:
        orm_mode = True
