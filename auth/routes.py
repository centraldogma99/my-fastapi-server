from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from .models import Token, User, UserToCreate
from .security import (
    authenticate_user,
    create_access_token,
    get_current_active_admin_user,
    get_current_active_user,
    get_user_by_username as get_user_by_username_db,
    create_user as create_user_db,
    remove_user as remove_user_db,
)


router = APIRouter(
    tags=["authentication"],
)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 유저이름 또는 비번임",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(
        access_token=create_access_token(data={"sub": user.username}),
        token_type="bearer",
    )


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@router.get("/users/{username}")
async def get_user_by_id(
    username: str,
    _: Annotated[
        User,
        Depends(get_current_active_admin_user),
    ],
):
    return get_user_by_username_db(username)


@router.put("/users")
async def create_user(
    user: UserToCreate, _: Annotated[User, Depends(get_current_active_admin_user)]
):
    return create_user_db(user)


@router.delete("/users/{username}")
async def delete_user(
    username: str, _: Annotated[User, Depends(get_current_active_admin_user)]
):
    return remove_user_db(username)
