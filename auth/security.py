from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import jwt
from fastapi import Depends, HTTPException, status
from typing import Annotated
from .models import User, UserInDB
import os
from dotenv import load_dotenv
import sqlite3
from .models import UserToCreate
from config import DB_NAME


def get_user_by_username(username: str):
    with sqlite3.connect(DB_NAME) as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()


def create_user(user: UserToCreate):
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            (user.username, get_password_hash(user.plain_password)),
        )
        connect.commit()
        return cursor.lastrowid


def remove_user(username: str):
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        connect.commit()
        return cursor.lastrowid


load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(username: str):
    user = get_user_by_username(username)
    if user:
        return UserInDB(**user)


def authenticate_user(username: str, password: str):
    userFromDB = get_user(username)
    if not userFromDB:
        return False
    if not verify_password(password, userFromDB.hashed_password):
        return False
    return userFromDB


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰 검증 실패!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
