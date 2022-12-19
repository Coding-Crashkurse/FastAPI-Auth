from sqlalchemy import Boolean, Column, Enum, Integer, String

from .database import Base
from .schemas import Roles


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(Roles), default=Roles.user.value)
