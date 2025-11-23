"""
System Settings Model - Configurações do sistema
"""
from app import db
from datetime import datetime


class SystemSettings(db.Model):
    """Configurações do sistema"""
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text)
    description = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<SystemSettings {self.key}={self.value}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AuditLog(db.Model):
    """Log de auditoria de ações administrativas"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)  # 'create_user', 'block_ip', etc
    target = db.Column(db.String(200))  # Alvo da ação
    details = db.Column(db.Text)  # JSON com detalhes
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action} by user {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'target': self.target,
            'details': self.details,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


# Helper functions
def get_setting(key, default=None):
    """Obtém uma configuração do sistema"""
    setting = SystemSettings.query.filter_by(key=key).first()
    return setting.value if setting else default


def set_setting(key, value, description=None, user_id=None):
    """Define uma configuração do sistema"""
    try:
        setting = SystemSettings.query.filter_by(key=key).first()
        
        if setting:
            setting.value = value
            setting.updated_by = user_id
            if description:
                setting.description = description
        else:
            setting = SystemSettings(
                key=key,
                value=value,
                description=description,
                updated_by=user_id
            )
            db.session.add(setting)
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao definir configuração: {e}")
        return False


def log_action(user_id, action, target=None, details=None, ip_address=None):
    """Registra uma ação no log de auditoria"""
    try:
        log = AuditLog(
            user_id=user_id,
            action=action,
            target=target,
            details=details,
            ip_address=ip_address
        )
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao registrar log: {e}")
        return False


def is_maintenance_mode():
    """Verifica se o site está em modo manutenção"""
    return get_setting('maintenance_mode', 'false') == 'true'


def set_maintenance_mode(enabled, user_id=None):
    """Ativa/desativa modo manutenção"""
    value = 'true' if enabled else 'false'
    result = set_setting('maintenance_mode', value, 'Site em modo manutenção', user_id)
    
    if result and user_id:
        log_action(user_id, 'maintenance_mode', 
                  target='system', 
                  details=f'Modo manutenção: {value}')
    
    return result
