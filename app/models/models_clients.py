import sqlite3
from flask import current_app

DATABASE_PATH = "data/database.db"
CLIENTS_DATABASE_PATH = "data/database_clients.db"


class User:

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password


def create_clients_database():
    conn = sqlite3.connect(CLIENTS_DATABASE_PATH)
    cursor = conn.cursor()

    # Cria a tabela 'user' no novo banco de dados de clientes (se não existir)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def init_app(app):
    # Configura o banco de dados principal
    app.config['DATABASE_PATH'] = DATABASE_PATH

    # Cria o banco de dados principal (se não existir)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    # Configura o banco de dados de clientes
    app.config['CLIENTS_DATABASE_PATH'] = CLIENTS_DATABASE_PATH

    # Cria o banco de dados de clientes (se não existir)
    create_clients_database()


# Exemplo de uso:
# from flask import Flask
# app = Flask(__name__)
# init_app(app)
