"""
User Models - ORM SQLAlchemy
"""
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """Modelo de usuário"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


def get_user_by_username(username):
    """Busca usuário pelo username"""
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    """Busca usuário pelo email"""
    return User.query.filter_by(email=email).first()


def create_user(username, email, password_hash, is_admin=False):
    """Cria um novo usuário"""
    try:
        user = User(
            username=username,
            email=email,
            password=password_hash,
            is_admin=is_admin
        )
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar usuário: {e}")
        return None
