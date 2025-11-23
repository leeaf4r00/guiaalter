"""
Admin Routes - Rotas administrativas
"""
from flask import render_template, Blueprint
from flask_login import login_required, current_user
from functools import wraps
from app.models.users import User
from app.models.tours import Tour

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
    # Fetch real data from database
    user_count = User.query.count()
    tour_count = Tour.query.count()
    # Assuming we might have a Reservation model later, for now 0
    reservation_count = 0 
    
    # Fetch recent users (limit 5)
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/paineladm.html', 
                           user_count=user_count, 
                           tour_count=tour_count, 
                           reservation_count=reservation_count,
                           recent_users=recent_users)
