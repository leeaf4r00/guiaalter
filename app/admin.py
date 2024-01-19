from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, logout_user, current_user
from app.users import get_user_by_username
from app.forms import RegistrationForm
from app.database import db
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def admin_dashboard():
    users = db.get_all_users()
    return render_template('admin.html',
                           username=current_user.username,
                           users=users)


@admin.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('routes.index'))


@admin.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        is_admin = False
        if form.username.data == "seu_usuario_admin" and db.count_admin_users() == 0:
            is_admin = True
        success = db.create_user(form.username.data, hashed_password, is_admin)
        if success:
            flash('Conta criada com sucesso!', 'success')
            if is_admin:
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('routes.login'))
        else:
            flash('Erro ao criar a conta.', 'error')
    return render_template('cadastro.html', title='Cadastro', form=form)
