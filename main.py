from fastapi import FastAPI
from auth import router as auth_router
from post import router as post_router
from db.init_db import init_db

init_db()

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(post_router, prefix="/post")
