from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from .models import User
from .database import get_db_connection, count_users

# Criação de um objeto Blueprint
routes = Blueprint('routes', __name__)

# Rota para a página inicial


@routes.route('/')
def index():
    user_count = count_users()
    return render_template('index.html', user_count=user_count)

# Rota para a página de login


@routes.route('/login', methods=['GET', 'POST'])
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
                user = User()
                user.id = result[0]
                login_user(user)
                return redirect(url_for('routes.index'))
            else:
                return render_template('login.html', error='Credenciais inválidas. Tente novamente.')
    return render_template('login.html')

# Rota para a página de pacotes


@routes.route('/pacotes')
def pacotes():
    return render_template('pacotes.html')


@routes.route('/contato')
def pacotes():
    return render_template('contato.html')

# Rota para a página "Sobre Nós"


@routes.route('/sobrenos')
def sobrenos():
    return render_template('sobrenos.html')

# Rota para realizar logout


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

# Rota protegida que requer autenticação


@routes.route('/admin')
@login_required
def admin():
    return render_template('admin.html', username=current_user.id)
