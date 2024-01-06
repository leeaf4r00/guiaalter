import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Caminho relativo para o banco de dados SQLite
DATABASE_PATH = os.path.join(os.getcwd(), "data", "database.db")


class User(UserMixin):
    def __init__(self, id, username, email, password, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

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


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def validate_login(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None


def create_user(username, password, is_admin=False):
    hashed_password = generate_password_hash(password)
    is_first_user = is_admin and count_users() == 0

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            (username, hashed_password, int(is_admin or is_first_user)),
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print("Erro ao inserir usuário: ", e)
        return False
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()
        if user_data:
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                is_admin=bool(user_data['is_admin']),
            )
    except sqlite3.Error as e:
        print("Erro ao buscar usuário: ", e)
        return None
    finally:
        conn.close()


def count_users():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print("Erro ao contar usuários: ", e)
        return 0
    finally:
        conn.close()


def count_admin_users():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print("Erro ao contar admins: ", e)
        return 0
    finally:
        conn.close()
