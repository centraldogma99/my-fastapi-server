import sqlite3
from datetime import datetime
from pydantic import BaseModel
from config import DB_NAME
from .models import Post


def write_post(post: Post):
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        current_time = datetime.now().isoformat()
        cursor.execute(
            """
        INSERT INTO posts (slug, contents, created_date)
        VALUES (?, ?, ?)
        """,
            (
                *post.model_dump().values(),
                current_time,
            ),
        )
        connect.commit()
        return cursor.lastrowid


def get_all_posts():
    with sqlite3.connect(DB_NAME) as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        return cursor.fetchall()


def get_post_by_id(post_id: int):
    with sqlite3.connect(DB_NAME) as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        return cursor.fetchone()


def remove_post(post_id: int):
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        connect.commit()
