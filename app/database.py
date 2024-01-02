import sqlite3
from flask import current_app


def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE_PATH'])
    conn.row_factory = sqlite3.Row
    return conn


def create_user(username, hashed_password):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        connection.commit()


def count_users():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        result = cursor.fetchone()
        return result[0] if result else 0
