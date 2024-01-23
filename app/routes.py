import sqlite3
from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.users import User, get_user_by_username
from app.forms import RegistrationForm
from app.database import db

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    user_count = db.count_users()
    return render_template('index.html', user_count=user_count)


@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password or not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"message": "Usuário e senha são obrigatórios e devem ser strings"}), 400

    user = get_user_by_username(username)

    if user and check_password_hash(user.password, password):
        user_object = User(user.id, user.username, user.email,
                           user.password, user.is_admin)
        login_user(user_object)

        if user.is_admin:
            return jsonify({"redirect": url_for('routes.admin')})
        else:
            return jsonify({"redirect": url_for('routes.index')})
    else:
        return jsonify({"message": "Usuário ou senha inválidos"}), 401


@routes.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        is_admin = form.username.data == "seu_usuario_admin" and db.count_admin_users() == 0
        success = db.create_user(form.username.data, hashed_password, is_admin)
        flash('Conta criada com sucesso!' if success else 'Erro ao criar a conta.',
              'success' if success else 'error')
        return redirect(url_for('routes.cadastro_bem_sucedido' if success else 'routes.register'))

    return render_template('cadastro.html', title='Cadastro', form=form)


@routes.route('/reservas', methods=['GET', 'POST'])
def reservas():
    return render_template('reservas.html')


@routes.route('/pacotes')
def pacotes():
    return render_template('pacotes.html')


@routes.route('/buffets')
def buffets():
    return render_template('buffets.html')


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


@routes.route('/explorealter')
def explorealter():
    return render_template('explorealter.html')


@routes.route('/mapaalter')
def mapaalter():
    return render_template('mapaalter.html')


@routes.route('/pessoascompraram')
def pessoascompraram():
    return render_template('pessoascompraram.html')


@routes.route('/conhecaalter')
def conhecaalter():
    return render_template('conhecaalter.html')


@routes.route('/souvenir')
def souvenir():
    return render_template('souvenir.html')


@routes.route('/sejanossoparceiro')
def sejanossoparceiro():
    return render_template('sejanossoparceiro.html')


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))


@routes.route('/admin')
def admin():
    return render_template('admin.html')


@routes.route('/rioarapiuns')
def rioarapiuns():
    return render_template('rioarapiuns.html')


@routes.route('/lagoverde')
def lagoverde():
    return render_template('lagoverde.html')


@routes.route('/descendoorio')
def descendoorio():
    return render_template('descendoorio.html')


@routes.route('/subindoorio')
def subindoorio():
    return render_template('subindoorio.html')


@routes.route('/tourdestaques')
def tourdestaques():
    return render_template('tourdestaques.html')


@routes.route('/depoimentos')
def depoimentos():
    return render_template('depoimentos.html')


@routes.route('/cadastro_bem_sucedido')
def cadastro_bem_sucedido():
    return render_template('cadastro_backend.html')


@routes.route('/rotas')
def rotas():
    return render_template('rotas.html')


@routes.route('/user_list')
def user_list():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username,
                  "email": user.email} for user in users]
    return jsonify({"users": user_list})

