import os
from app.routes import routes
from flask import Flask
from flask_login import LoginManager, UserMixin

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
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


# Importa as rotas
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
