import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Caminho para o banco de dados SQLite
DATABASE_PATH = "data/database.db"


class User(UserMixin):
    def __init__(self, id, username, email, password, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
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
    return conn


def validate_login(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None, False


def create_user(username, password, is_admin=False):
    hashed_password = generate_password_hash(password)
    is_first_user = is_admin and count_users() == 0
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if is_first_user:
            cursor.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, 1)",
                (username, hashed_password),
            )
        else:
            cursor.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                (username, hashed_password, int(is_admin)),
            )

        conn.commit()

    except sqlite3.Error as e:
        print("Erro ao inserir usuário: ", e)

    finally:
        conn.close()


def get_user_by_username(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))

        user_data = cursor.fetchone()

        if user_data:
            return User(
                id=user_data[0],
                username=user_data[1],
                email=user_data[2],
                password=user_data[3],
                is_admin=bool(user_data[4]),
            )

    except sqlite3.Error as e:
        print("Erro ao buscar usuário: ", e)

    finally:
        conn.close()


def count_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")

        count = cursor.fetchone()[0]

        return count

    except sqlite3.Error as e:
        print("Erro ao contar usuários: ", e)

    finally:
        conn.close()


def count_admin_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM users WHERE is_admin = 1")

        count = cursor.fetchone()[0]

        return count

    except sqlite3.Error as e:
        print("Erro ao contar admins: ", e)

    finally:
        conn.close()
