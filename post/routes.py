from fastapi import APIRouter

from .db import (
    Post,
    get_all_posts,
    get_post_by_id as get_post_from_db,
    remove_post,
    write_post,
)


router = APIRouter(
    tags=["posts"],
)


@router.get("/")
async def get_posts():
    return get_all_posts()


@router.get("/{post_id}")
async def get_post_by_id(post_id: int):
    post = get_post_from_db(post_id)
    if post is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")
    return post


@router.post("/")
async def create_post(post: Post):
    return write_post(post)


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    return remove_post(post_id)
