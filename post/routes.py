from fastapi import APIRouter

from .db import Post, get_all_posts, remove_post, write_post


router = APIRouter(
    tags=["posts"],
)


@router.get("/")
async def get_posts():
    return get_all_posts()


@router.get("/{post_id}")
async def get_post_by_id(post_id: int):
    return get_post_by_id(post_id)


@router.post("/")
async def create_post(post: Post):
    return write_post(post)


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    return remove_post(post_id)
