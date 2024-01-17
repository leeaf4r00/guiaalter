import os
from flask import Flask, render_template
from flask_login import LoginManager, UserMixin
from app.models.user import get_user_by_username
from app.routes import routes
from app.routes_tours import routes_tours
from app.routes_admin import routes_admin
from app.database import db

app = Flask(__name__)

# Configurações
app.config['DATABASE_PATH'] = "data/database.db"
app.config['SECRET_KEY'] = os.environ.get(
    'FLASK_SECRET_KEY', 'sua_chave_secreta')

# Configuração do sistema de login
login_manager = LoginManager(app)
login_manager.login_view = 'routes.login'

# Classe de usuário para Flask-Login


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    # Use a função do banco de dados para obter o usuário
    user_data = db.get_user_by_username(user_id)
    if user_data:
        return User(user_id=user_data[0])
    return None


# Importa e registra as rotas
app.register_blueprint(routes)
app.register_blueprint(routes_tours)
app.register_blueprint(routes_admin)

# Configuração de tratamento de erro 404


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get("FLASK_DEBUG", False),
            use_reloader=True, host='0.0.0.0', port=port)
