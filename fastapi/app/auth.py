from fastapi import Depends, HTTPException, Security, status, Cookie
from typing import Union, Any, Optional

from datetime import datetime, timedelta
import os
from passlib.context import CryptContext

from fastapi_jwt import (
    JwtAccessBearer,
    JwtAccessBearerCookie,
    JwtAuthorizationCredentials,
    JwtRefreshBearerCookie
)

SECRET_KEY = os.getenv('SECRET_KEY')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Read verification token from bearer header only
verification_security = JwtAccessBearer(
    secret_key=SECRET_KEY,
    auto_error=False,
    access_expires_delta=timedelta(minutes=5)  # change access token validation timedelta
)

# Read access token from bearer header and cookie (bearer priority)
access_security = JwtAccessBearerCookie(
    secret_key=SECRET_KEY,
    auto_error=False,
    access_expires_delta=timedelta(hours=1)  # change access token validation timedelta
)

# Read refresh token from bearer header and cookie (bearer priority)
refresh_security = JwtRefreshBearerCookie(
    secret_key=SECRET_KEY, 
    auto_error=True  # automatically raise HTTPException: HTTP_401_UNAUTHORIZED 
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def get_credentials(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return credentials


def get_credentials_refresh(credentials: JwtAuthorizationCredentials = Security(refresh_security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return credentials


def get_current_user(credentials: str = Depends(get_credentials)):
    if (username := credentials["username"]) is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid username"
        )
    return username


def check_active(credentials: str = Depends(get_credentials)):
    if credentials["is_active"] is not True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please activate your Account first"
        )
    return


def check_admin(credentials: str = Depends(get_credentials)):
    if credentials["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this route"
        )
    return
