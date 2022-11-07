from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from typing import Union, Any

from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scheme_name="JWT"
)


# def create_access_token(user: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.utcnow() + expires_delta
#     else:
#         expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode = {"exp": expires_delta, "sub": str(user)}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
#     return encoded_jwt


def create_access_token(user):
    try:
        data = {
            "sub": user.username,
            "email": user.email,
            "role": user.role.value,
            "active": user.is_active,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_token(token):
    try:
        payload = jwt.decode(token, key=SECRET_KEY)
        return payload
    except:
        raise Exception("Wrong token")


def check_active(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    active = payload.get("active")
    if not active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please activate your Account first",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return payload


def check_admin(payload: dict = Depends(check_active)):
    role = payload.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this route",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return (f"User is: {role}")
