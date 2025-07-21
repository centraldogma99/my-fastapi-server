import sqlite3
from config import DB_NAME

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
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            disabled BOOLEAN NOT NULL DEFAULT 0,
        )
    """
    )
    cursor.execute("SELECT name FROM sqlite_master")
    print(cursor.fetchall())
