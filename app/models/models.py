import os
import shutil
import sqlite3


def restore_database(backup_file_path, database_path):
    """
    Restaura o banco de dados a partir de um arquivo de backup.
    """
    if os.path.exists(backup_file_path):
        shutil.copy(backup_file_path, database_path)
        print("Database restored from backup.")
    else:
        print("Backup file not found.")


def create_database(database_path):
    """
    Cria o banco de dados e tabelas necessárias.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Aqui você pode adicionar comandos SQL para criar suas tabelas
    # Por exemplo:
    # cursor.execute('''CREATE TABLE IF NOT EXISTS users (...)''')

    conn.commit()
    conn.close()


def init_database(database_path):
    """
    Inicializa o banco de dados.
    """
    if not os.path.exists(database_path):
        create_database(database_path)
    else:
        print("Database already exists.")


# Exemplo de como você pode usar essas funções
if __name__ == '__main__':
    database_path = 'data/database.db'
    backup_file_path = 'data/database_backup.db'

    # Restaura o banco de dados a partir de um backup
    restore_database(backup_file_path, database_path)

    # Inicializa o banco de dados
    init_database(database_path)
