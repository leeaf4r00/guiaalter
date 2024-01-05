import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Defina a variável DATABASE_PATH em algum lugar, por exemplo, no início do seu script.
DATABASE_PATH = "data/database.db"


class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


def get_database_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_user(username, password):
    hashed_password = generate_password_hash(password)
    try:
        connection = get_database_connection()
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
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, password FROM users WHERE username = ?",
            (username,))
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


def count_users():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(id) FROM users")
        return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()
