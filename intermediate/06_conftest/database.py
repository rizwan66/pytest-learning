import sqlite3
from contextlib import contextmanager


class Database:
    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'user'
            )
        """)
        self.conn.commit()

    def insert_user(self, name, email, role="user"):
        cursor = self.conn.execute(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
            (name, email, role)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_email(self, email):
        row = self.conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        return dict(row) if row else None

    def get_all_users(self):
        rows = self.conn.execute("SELECT * FROM users").fetchall()
        return [dict(r) for r in rows]

    def delete_user(self, email):
        self.conn.execute("DELETE FROM users WHERE email = ?", (email,))
        self.conn.commit()

    def close(self):
        self.conn.close()
