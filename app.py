from flask import Flask
from flask_login import LoginManager

# Importações do modelo User e funções auxiliares do database.py
from app.models.user import User, get_user_by_username
from app.database import create_user, count_users


def create_app():
    app = Flask(__name__)

    # Configurações
    app.config['DATABASE_PATH'] = "data/database.db"
    app.config['SECRET_KEY'] = 'NOVA_CHAVE_SECRETA'  # Atualizada

    login_manager = LoginManager(app)
    login_manager.login_view = 'routes.login'

    @login_manager.user_loader
    def load_user(username):
        user_data = get_user_by_username(username)

        if user_data:
            return User(
                user_id=user_data[0],
                username=user_data[1],
                email=user_data[2],
                password=user_data[3]
            )

        return None

    # Blueprints
    from app.routes import routes
    from app.routes_tours import routes_tours

    app.register_blueprint(routes)
    app.register_blueprint(routes_tours)

    # Configurar as funções do database.py para serem acessíveis pelo aplicativo
    app.config['create_user'] = create_user
    app.config['count_users'] = count_users

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
