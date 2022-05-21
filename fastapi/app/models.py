from sqlalchemy import Boolean, Column, Enum, Integer, String

from .database import Base
from .schemas import Roles


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=False, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(Roles), default="user")
