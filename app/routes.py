from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from .database import count_users
from .user import validate_login  # Importação da função validate_login

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    user_count = count_users()
    return render_template('index.html', user_count=user_count)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = validate_login(username, password)
        if user_id:
            user = User()
            user.id = user_id
            login_user(user)
            return redirect(url_for('routes.index'))
        else:
            return render_template('login.html', error='Credenciais inválidas. Tente novamente.')
    return render_template('login.html')


@routes.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Implemente a lógica de cadastro aqui
        pass
    return render_template('cadastro.html')


@routes.route('/reservas', methods=['GET', 'POST'])
def reservas():
    if request.method == 'POST':
        # Implemente a lógica de reservas aqui
        pass
    return render_template('reservas.html')


@routes.route('/pacotes')
def pacotes():
    return render_template('pacotes.html')


@routes.route('/hotels')
def hotels():
    return render_template('hotels.html')


@routes.route('/passeios')
def passeios():
    return render_template('passeios.html')


@routes.route('/contato')
def contato():
    return render_template('contato.html')


@routes.route('/veiculos')
def veiculos():
    return render_template('veiculos.html')


@routes.route('/sobrenos')
def sobrenos():
    return render_template('sobrenos.html')


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))


@routes.route('/admin')
@login_required
def admin():
    return render_template('admin.html', username=current_user.id)


@routes.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
