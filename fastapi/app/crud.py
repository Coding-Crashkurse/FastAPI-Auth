from sqlalchemy.orm import Session

from . import auth, models, schemas


def create_user(db: Session, user: schemas.UserSchema):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.UserModel(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role=user.role.value,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.UserModel).all()


def get_users_by_username(db: Session, username: str):
    return (
        db.query(models.UserModel).filter(models.UserModel.username == username).first()
    )
