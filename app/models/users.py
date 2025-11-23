"""
User Models - ORM SQLAlchemy
Enhanced with role levels and status management
"""
from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    """Modelo de usuário com níveis de acesso"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    
    # Role-based access control
    # Roles: 'admin', 'partner', 'user'
    role = db.Column(db.String(20), default='user', nullable=False)
    
    # Status: 'active', 'blocked', 'pending'
    status = db.Column(db.String(20), default='active', nullable=False)
    
    # Legacy field for backward compatibility
    is_admin = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Additional info
    full_name = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'is_admin': self.is_admin or self.role == 'admin',
            'full_name': self.full_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def is_active_user(self):
        """Verifica se usuário está ativo"""
        return self.status == 'active'
    
    def has_role(self, role):
        """Verifica se usuário tem determinado role"""
        return self.role == role
    
    def is_administrator(self):
        """Verifica se é administrador"""
        return self.role == 'admin' or self.is_admin


class BlockedIP(db.Model):
    """Modelo para IPs bloqueados"""
    __tablename__ = 'blocked_ips'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), unique=True, nullable=False, index=True)
    reason = db.Column(db.String(500))
    blocked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    blocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # Null = permanente
    
    def __repr__(self):
        return f'<BlockedIP {self.ip_address}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'reason': self.reason,
            'blocked_at': self.blocked_at.isoformat() if self.blocked_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }


# Helper functions
def get_user_by_username(username):
    """Busca usuário pelo username"""
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    """Busca usuário pelo email"""
    return User.query.filter_by(email=email).first()


def create_user(username, email, password_hash, role='user', is_admin=False, **kwargs):
    """Cria um novo usuário"""
    try:
        # Se is_admin=True, força role='admin'
        if is_admin:
            role = 'admin'
        
        user = User(
            username=username,
            email=email,
            password=password_hash,
            role=role,
            is_admin=is_admin,
            **kwargs
        )
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar usuário: {e}")
        return None


def is_ip_blocked(ip_address):
    """Verifica se IP está bloqueado"""
    from datetime import datetime
    blocked = BlockedIP.query.filter_by(ip_address=ip_address).first()
    
    if not blocked:
        return False
    
    # Verifica se bloqueio expirou
    if blocked.expires_at and blocked.expires_at < datetime.utcnow():
        db.session.delete(blocked)
        db.session.commit()
        return False
    
    return True


def block_ip(ip_address, reason=None, blocked_by_user_id=None, expires_at=None):
    """Bloqueia um IP"""
    try:
        blocked = BlockedIP(
            ip_address=ip_address,
            reason=reason,
            blocked_by=blocked_by_user_id,
            expires_at=expires_at
        )
        db.session.add(blocked)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao bloquear IP: {e}")
        return False


def unblock_ip(ip_address):
    """Desbloqueia um IP"""
    try:
        blocked = BlockedIP.query.filter_by(ip_address=ip_address).first()
        if blocked:
            db.session.delete(blocked)
            db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao desbloquear IP: {e}")
        return False

