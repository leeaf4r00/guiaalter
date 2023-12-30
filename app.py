from flask import Flask, render_template, request, redirect, url_for, g
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DATABASE = "database.db"

# Função para conectar ao banco de dados SQLite


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Função para contar o número de usuários no banco de dados


def count_users():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        result = cursor.fetchone()
        return result[0] if result else 0

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
                # Se a autenticação for bem-sucedida, definir a variável de sessão 'is_admin' como True
                g.is_admin = True
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Credenciais inválidas. Tente novamente.')
    return render_template('login.html')

# Rota para a página "Sobre Nós"


@app.route('/sobrenos')
def sobrenos():
    # Adicione a função get_images conforme a necessidade
    img_paths_sobrenos = get_images('img')
    return render_template('sobrenos.html', img_paths=img_paths_sobrenos)


if __name__ == '__main__':
    app.run(debug=True)
