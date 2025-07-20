import sqlite3
from datetime import datetime
from .constants import DB_NAME
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    description: str | None = None
    content: str


def write_post(post: Post):
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        # 현재 시간을 ISO 8601 형식으로 가져오기
        current_time = datetime.now().isoformat()

        cursor.execute(
            """
        INSERT INTO posts (title, description, content, created_date)
        VALUES (?, ?, ?, ?)
        """,
            (
                *post.model_dump().values(),
                current_time,
            ),
        )
        connect.commit()


def get_all_posts():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM posts")
        return cursor.fetchall()


def get_post_by_id(post_id: int):
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECCT * FROM posts WHERE id = ?", (post_id,))
        return cursor.fetchone()


def remove_post(post_id: int):
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        connect.commit()
