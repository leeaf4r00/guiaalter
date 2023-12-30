from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configurações
app.config['DATABASE_PATH'] = "data/database.db"
app.config['SECRET_KEY'] = os.environ.get(
    'FLASK_SECRET_KEY', 'sua_chave_secreta')

# Função para conectar ao banco de dados SQLite


def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE_PATH'])
    conn.row_factory = sqlite3.Row

    with conn:
        cursor = conn.cursor()

        # Verifica se a tabela 'users' existe
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone()

        if not table_exists:
            # Cria a tabela 'users' se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

            # Adiciona um usuário inicial
            hashed_password = generate_password_hash(
                '@$RA!8421789Ra33', method='sha256', salt_length=16)
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           ('rafaelfernandes', hashed_password))

    return conn

# Função para contar o número de usuários no banco de dados


def count_users():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        result = cursor.fetchone()
        return result[0] if result else 0

# Função para obter as imagens da pasta 'img'


def get_images(folder):
    folder_path = os.path.join('static', 'img', folder)
    images = [os.path.join(folder_path, f) for f in os.listdir(
        folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return images

# Rota para a página inicial


@app.route('/')
def index():
    user_count = count_users()
    return render_template('index.html', user_count=user_count)

# Rota para a página de login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result and check_password_hash(result[0], password):
                # Se a autenticação for bem-sucedida, armazenar na sessão
                session['is_admin'] = True
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Credenciais inválidas. Tente novamente.')
    return render_template('login.html')

# Rota para a página "Sobre Nós"


@app.route('/sobrenos')
def sobrenos():
    img_paths_sobrenos = get_images('img')
    return render_template('sobrenos.html', img_paths=img_paths_sobrenos)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get("FLASK_DEBUG", False),
            use_reloader=True, host='0.0.0.0', port=port)
