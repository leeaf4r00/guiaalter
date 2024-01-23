import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Caminho relativo para o banco de dados SQLite
DATABASE_PATH = os.path.join(os.getcwd(), "data", "database.db")

# Função para criar e inicializar a tabela de usuários no banco de dados


def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Criação da tabela de usuários se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


# Inicializa o banco de dados chamando a função init_db
init_db()

# Classe de usuário para Flask-Login


class User(UserMixin):
    def __init__(self, id, username, email, password, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Função para obter uma conexão com o banco de dados


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar um novo usuário


def create_user(username, email, password, is_admin=False):
    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            (username, email, hashed_password, int(is_admin)),
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print("Erro ao inserir usuário: ", e)
        return False
    finally:
        conn.close()

# Função para obter um usuário pelo nome de usuário


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

# Função para validar as credenciais de login


def validate_login(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None

# Função para contar o número total de usuários


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

# Função para contar o número de administradores


def count_admin_users():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print("Erro ao contar administradores: ", e)
        return 0
    finally:
        conn.close()

# Classe UserDatabase para gerenciar usuários em memória


class UserDatabase:
    def __init__(self):
        self.users = {}
        self.user_id_counter = 1

    def create_user(self, username, password, is_admin=False):
        user_id = self.user_id_counter
        self.users[user_id] = {
            'id': user_id,
            'username': username,
            'password': password,
            'is_admin': is_admin
        }
        self.user_id_counter += 1
        return user_id

    def get_user_by_id(self, user_id):
        return self.users.get(user_id)

    def get_user_by_username(self, username):
        for user in self.users.values():
            if user['username'] == username:
                return user
        return None

    def count_admin_users(self):
        count = 0
        for user in self.users.values():
            if user['is_admin']:
                count += 1
        return count

    def count_users(self):
        return len(self.users)
