from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
from pydantic import EmailStr


class Roles(Enum):
    user = "user"
    admin = "admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    username: str
    is_active: bool
    role: Roles
    name: str = Field(index=True)
