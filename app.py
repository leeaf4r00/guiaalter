import os
from app.routes import routes
from app.routes_tours import routes_tours  # Adicione esta linha
from flask import Flask
from flask_login import LoginManager, UserMixin, login_required
from app.models.user import get_user_by_username

app = Flask(__name__)

# Configurações
app.config['DATABASE_PATH'] = "data/database.db"
app.config['SECRET_KEY'] = os.environ.get(
    'FLASK_SECRET_KEY', 'sua_chave_secreta')

# Configuração do sistema de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Classe de usuário para Flask-Login


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_username(user_id)
    if user_data:
        return User(user_id=user_data[0])
    return None


# Importa e registra as rotas
app.register_blueprint(routes)
app.register_blueprint(routes_tours)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get("FLASK_DEBUG", False),
            use_reloader=True, host='0.0.0.0', port=port)
