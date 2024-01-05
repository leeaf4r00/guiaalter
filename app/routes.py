from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app.models.user import User, validate_login
from app.models.user import User, get_user_by_username
from app.forms import RegistrationForm
from app.database import db
from app.forms import RegistrationForm

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    user_count = db.count_users()  # Use a função 'count_users' da instância 'db'
    return render_template('index.html', user_count=user_count)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            flash('Informe o nome de usuário', 'error')
            return redirect(url_for('routes.login'))

        if not password:
            flash('Informe a senha', 'error')
            return redirect(url_for('routes.login'))

        user = get_user_by_username(username)

        if not user:
            flash('Usuário não encontrado', 'error')
            return redirect(url_for('routes.login'))

        if user.check_password(password):
            user_object = User(user.id, user.username,
                               user.email, user.password, user.is_admin)

            if login_user(user_object):
                if user.is_admin:
                    # Redirecionar usuário administrativo
                    return redirect(url_for('routes.admin'))
                else:
                    # Redirecionar usuário normal
                    return redirect(url_for('routes.index'))
            else:
                flash('Erro ao fazer login', 'error')
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')

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

            # Redirecionar com base no nível de permissão
            if is_admin:
                return redirect(url_for('routes.admin'))
            else:
                return redirect(url_for('routes.login'))
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


@routes.route('/cadastro_backend')
def cadastro_backend():
    return render_template('cadastro_backend.html')
