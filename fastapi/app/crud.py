from sqlalchemy.orm import Session
from typing import List, Optional
from . import auth, models, schemas
import uuid

def get_user(db: Session, id: str):
    return db.query(models.UserModel).filter(models.UserModel.id == id).first()

def create_user(db: Session, user: schemas.UserRegister):
    hashed_password = auth.get_password_hash(user.password)
    id = uuid.uuid4()
    while get_user(db=db,id=str(id)):
        id = uuid.uuid4()
    # import pdb; pdb.set_trace()    
    db_user = models.UserModel(
        id=str(id),
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_active=user.is_active,
        role=user.role.value,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    users: List[schemas.UserDB] = db.query(models.UserModel).all()
    return users

def get_users_by_username(db: Session, username: str):
    user: schemas.UserDB = db.query(models.UserModel).filter(models.UserModel.username == username).first()
    return user