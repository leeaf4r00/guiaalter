from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import User, validate_login
from app.forms import RegistrationForm
# Importe a função count_users do arquivo app.database
from app.database import count_users

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


@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = form.password.data
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password, user_type=form.user_type.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('routes.login'))
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
@login_required
def admin():
    return render_template('admin.html', username=current_user.id)


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
