from app.routes_admin import routes_admin
from app.routes_tours import routes_tours
from app.routes import routes
import os
from flask import Flask, render_template
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações
app.config['DATABASE_PATH'] = 'data/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
app.config['SECRET_KEY'] = "leeafar:420"

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Configuração do sistema de login
login_manager = LoginManager(app)
login_manager.login_view = 'routes.login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_current_year():
    """Inject current year into all templates"""
    from datetime import datetime
    return {'current_year': datetime.now().year}


# Importa e registra as blueprints

app.register_blueprint(routes)
app.register_blueprint(routes_tours)
app.register_blueprint(routes_admin)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get("FLASK_DEBUG", False),
            use_reloader=True, host='0.0.0.0', port=port)
