from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from typing import Optional
import os

from . import oauth_cookie

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

from datetime import datetime, timedelta

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = oauth_cookie.OAuth2PasswordBearerWithCookie(tokenUrl="login")


def create_access_token(user):
    try:
        claims = {
            "sub": user.username,
            "email": user.email,
            "role": user.role.value,
            "active": user.is_active,
            "exp": datetime.utcnow() + timedelta(minutes=120),
        }
        return jwt.encode(claims=claims, key=SECRET_KEY, algorithm=ALGORITHM)
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
    # import pdb; pdb.set_trace()
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
        return sub
