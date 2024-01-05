import sqlite3

DATABASE_PATH = "data/clients.db"


def create_clients_database():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            email TEXT,
            telefone TEXT
        )
    ''')
    connection.commit()
    connection.close()


def add_client(nome, email, telefone):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO clients (nome, email, telefone) VALUES (?, ?, ?)",
                   (nome, email, telefone))
    connection.commit()
    connection.close()

# Aqui você pode adicionar mais funções conforme necessário,
# como para buscar ou atualizar dados de clientes.
