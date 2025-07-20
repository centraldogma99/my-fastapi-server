import sqlite3
from constants import DB_NAME

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
    cursor.execute("SELECT name FROM sqlite_master")
    print(cursor.fetchall())
