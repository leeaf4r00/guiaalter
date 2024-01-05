from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


def create_clients_database(app):
    # Configura o banco de dados para usar o novo banco de dados de clientes
    app.config['SQLALCHEMY_BINDS'] = {
        'clients': 'sqlite:///data/database_clients.db'
    }
    db.init_app(app)

    # Cria as tabelas no novo banco de dados de clientes (se não existirem)
    with app.app_context():
        db.create_all(bind='clients')


def init_app(app):
    # Inicializa o aplicativo Flask com as configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
    db.init_app(app)

    # Cria e inicializa o banco de dados de clientes
    create_clients_database(app)
