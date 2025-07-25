from pydantic import BaseModel
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    username: str
    role: UserRole = UserRole.USER  # 기본값: 일반 사용자
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class UserToCreate(BaseModel):
    username: str
    plain_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
