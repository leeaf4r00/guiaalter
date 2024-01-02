import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_PATH = "data/database.db"


def create_user(username, password):
    hashed_password = generate_password_hash(password)
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        connection.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()


def get_user_by_username(username):
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, password FROM users WHERE username = ?", (username,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()


def validate_login(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user[1], password):
        return user[0]  # Retornar ID do usuário
    return None
