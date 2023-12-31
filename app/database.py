import sqlite3


class Database:

    def __init__(self, app=None):
        self.conn = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conn = sqlite3.connect(app.config['DATABASE_PATH'])
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn is not None:
            self.conn.close()

    def init_db(self):
        if self.conn is not None:
            # Cria tabela users com uma coluna adicional 'is_admin'
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    is_admin INTEGER NOT NULL DEFAULT 0
                )
            ''')

            # Cria outras tabelas conforme necessário

            self.conn.commit()

    def create_user(self, username, hashed_password, is_admin=False):
        if self.conn is not None:
            try:
                self.conn.execute(
                    'INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)',
                    (username, hashed_password, int(is_admin))
                )
                self.conn.commit()
                return True
            except sqlite3.Error:
                return False

    def get_user_by_username(self, username):
        if self.conn is not None:
            cursor = self.conn.execute(
                'SELECT * FROM users WHERE username = ?', (username,)
            )
            return cursor.fetchone()

    def count_admin_users(self):
        if self.conn is not None:
            cursor = self.conn.execute(
                'SELECT COUNT(*) FROM users WHERE is_admin = 1')
            result = cursor.fetchone()
            return result[0] if result else 0

    def count_users(self):
        if self.conn is not None:
            cursor = self.conn.execute('SELECT COUNT(*) FROM users')
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_all_users(self):
        if self.conn is not None:
            cursor = self.conn.execute('SELECT * FROM users')
            return cursor.fetchall()


# Instância global do banco de dados
db = Database()
