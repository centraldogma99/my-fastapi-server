import os
import sqlite3

from auth.security import get_password_hash
from config import DB_NAME


def init_db():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                created_date TEXT NOT NULL DEFAULT (datetime('now')),
                title TEXT NOT NULL,
                description TEXT,
                content TEXT NOT NULL
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL PRIMARY KEY,
                hashed_password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                disabled BOOLEAN NOT NULL DEFAULT 0
            )
        """
        )
        hashed_password = get_password_hash(os.getenv("ADMIN_PASSWORD"))
        print(hashed_password)
        cursor.execute(
            "INSERT INTO users (username, hashed_password, role, disabled) VALUES ('admin', ?, 'admin', 0)",
            (hashed_password,),
        )
        connect.commit()
