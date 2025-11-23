"""
Admin Routes - Rotas administrativas
"""
from flask import render_template, Blueprint
from flask_login import login_required, current_user
from functools import wraps

routes_admin = Blueprint('routes_admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator para verificar se o usuário é admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            from flask import abort
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@routes_admin.route('/')
@routes_admin.route('/painel')
@admin_required
def painel():
    """Painel administrativo"""
    return render_template('admin/paineladm.html')
