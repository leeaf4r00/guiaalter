from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app.models.user import User, validate_login
from app.models.user import User, get_user_by_username
from app.forms import RegistrationForm
from app.database import db
from app.forms import RegistrationForm
from flask import jsonify

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    user_count = db.count_users()  # Use a função 'count_users' da instância 'db'
    return render_template('index.html', user_count=user_count)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obter dados enviados pelo cliente em formato JSON
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            # Retorna um erro se o usuário ou senha não forem fornecidos
            return jsonify({"message": "Usuário e senha são obrigatórios"}), 400

        user = get_user_by_username(username)

        if user and check_password_hash(user.password, password):
            # Cria um objeto User para gerenciar o login
            user_object = User(user.id, user.username,
                               user.email, user.password, user.is_admin)
            login_user(user_object)

            # Redireciona para a página apropriada, dependendo do tipo de usuário
            if user.is_admin:
                return jsonify({"redirect": url_for('routes.admin')})
            else:
                return jsonify({"redirect": url_for('routes.index')})
        else:
            # Retorna um erro se as credenciais forem inválidas
            return jsonify({"message": "Usuário ou senha inválidos"}), 401

    # Renderiza a página de login para métodos GET
    return render_template('login.html')


@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data)  # Hash da senha
        is_admin = False
        if form.username.data == "seu_usuario_admin" and db.count_admin_users() == 0:
            is_admin = True
        # Usando create_user
        # Use a função 'create_user' da instância 'db'
        success = db.create_user(form.username.data, hashed_password, is_admin)
        if success:
            flash('Conta criada com sucesso!', 'success')

            # Redireciona para a página de cadastro bem-sucedido
            return redirect(url_for('routes.cadastro_bem_sucedido'))

        else:
            flash('Erro ao criar a conta.', 'error')
    return render_template('cadastro.html', title='Cadastro', form=form)


@routes.route('/reservas', methods=['GET', 'POST'])
def reservas():
    # Lógica de reservas
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
    # Lógica da visualização da página de administração
    return render_template('admin.html')


@routes.route('/rioarapiuns')
def rioarapiuns():
    # Aqui você pode adicionar qualquer lógica adicional necessária
    return render_template('rioarapiuns.html')


@routes.route('/lagoverde')
def lagoverde():
    # Aqui você pode adicionar qualquer lógica adicional necessária
    return render_template('lagoverde.html')


@routes.route('/descendoorio')
def descendoorio():
    # Aqui você pode adicionar qualquer lógica adicional necessária
    return render_template('descendoorio.html')


@routes.route('/subindoorio')
def subindoorio():
    # Aqui você pode adicionar qualquer lógica adicional necessária
    return render_template('subindoorio.html')


@routes.route('/tourdestaques')
def tourdestaques():
    # Seu código para a página de destaques do tour aqui
    return render_template('tourdestaques.html')


@routes.route('/depoimentos')
def depoimentos():
    # Seu código para a página de depoimentos do tour aqui
    return render_template('depoimentos.html')


@routes.route('/cadastro_bem_sucedido')
def cadastro_bem_sucedido():
    return render_template('cadastro_backend.html')


@routes.route('/user_list')
def user_list():
    # Recupere a lista de usuários cadastrados do seu banco de dados
    users = [
        {"id": 1, "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": "user2", "email": "user2@example.com"},
        # Adicione mais usuários da sua base de dados
    ]

    # Retorne a lista de usuários em formato JSON
    return jsonify({"users": users})
