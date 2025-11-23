"""
Guia de Alter - Aplicação Flask
Inicialização da aplicação
"""
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

# Inicializa extensões
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    """Factory pattern para criar a aplicação Flask"""
    # Define o caminho base como o diretório pai de 'app'
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(__name__,
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    
    # Carrega configuração
    from app.config import config, setup_logging
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config.get(config_name, config['default']))
    
    # Configura logging
    setup_logging(app)
    app.logger.info(f'Iniciando aplicação em modo: {config_name}')
    
    # Inicializa extensões com a app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login_page'
    
    # Importa models
    from app.models.users import User
    from app.models.tours import Tour
    
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
    from app.routes_mobile_admin import routes_mobile_admin
    from app.routes_public import routes_public
    
    app.register_blueprint(routes)
    app.register_blueprint(routes_tours)
    app.register_blueprint(routes_admin)
    app.register_blueprint(routes_mobile_admin)
    app.register_blueprint(routes_public)
    
    app.logger.info('Blueprints registrados com sucesso')
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        app.logger.warning(f'Página não encontrada: {error}')
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Erro interno do servidor: {error}', exc_info=True)
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Cria tabelas do banco de dados
    with app.app_context():
        db.create_all()
        app.logger.info('Tabelas do banco de dados criadas/verificadas')
    
    return app
