from db.post import get_all_posts, remove_post, write_post, get_post_by_id, Post
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/posts")
async def get_posts():
    return get_all_posts()


@app.get("/posts/{post_id}")
async def get_post_by_id(post_id: int):
    return get_post_by_id(post_id)


@app.post("/posts")
async def create_post(post: Post):
    return write_post(post)


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    return remove_post(post_id)
