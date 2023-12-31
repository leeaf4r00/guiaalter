from .routes import routes
from .models import User
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['DATABASE_PATH'] = "data/database.db"
app.config['SECRET_KEY'] = 'sua_chave_secreta'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


app.register_blueprint(routes)
