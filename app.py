from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Configurações
app.config['DATABASE_PATH'] = "data/database.db"
app.config['SECRET_KEY'] = os.environ.get(
    'FLASK_SECRET_KEY', 'sua_chave_secreta')

# Configuração do sistema de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Classe de usuário para Flask-Login


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

# Função para conectar ao banco de dados SQLite


def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE_PATH'])
    conn.row_factory = sqlite3.Row
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

# Rota para servir arquivos estáticos do diretório 'static'


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

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
                'SELECT id, password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result and check_password_hash(result[1], password):
                # Se a autenticação for bem-sucedida, realizar login com Flask-Login
                user = User()
                user.id = result[0]
                login_user(user)
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Credenciais inválidas. Tente novamente.')
    return render_template('login.html')

# Rota para a página de pacotes


@app.route('/pacotes')
def pacotes():
    return render_template('pacotes.html')

# Rota para a página "Sobre Nós"


@app.route('/sobrenos')
def sobrenos():
    img_paths_sobrenos = get_images('img')
    return render_template('sobrenos.html', img_paths=img_paths_sobrenos)

# Rota para realizar logout


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Rota protegida que requer autenticação


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', username=current_user.id)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get("FLASK_DEBUG", False),
            use_reloader=True, host='0.0.0.0', port=port)
