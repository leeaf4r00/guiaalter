"""
Guia de Alter - Aplicação Flask
Inicialização da aplicação
"""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

# Inicializa extensões
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Factory pattern para criar a aplicação Flask"""
    # Define o caminho base como o diretório pai de 'app'
    import os
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(__name__,
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    
    # Configurações
    app.config['DATABASE_PATH'] = 'database.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'leeafar:420')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa extensões com a app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login_page'
    
    # Importa models
    from app.models.users import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Carrega usuário pelo ID"""
        return User.query.get(int(user_id))
    
    @app.context_processor
    def inject_current_year():
        """Injeta o ano atual em todos os templates"""
        from datetime import datetime
        return {'current_year': datetime.now().year}
    
    # Registra blueprints
    from app.routes import routes
    from app.routes_tours import routes_tours
    from app.routes_admin import routes_admin
    
    app.register_blueprint(routes)
    app.register_blueprint(routes_tours)
    app.register_blueprint(routes_admin)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        from flask import render_template
        return render_template('404.html'), 404
    
    # @app.errorhandler(500)
    # def internal_error(error):
    #     from flask import render_template
    #     db.session.rollback()
    #     return render_template('500.html'), 500
    
    # Cria tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app
