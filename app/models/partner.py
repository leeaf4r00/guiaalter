"""
Partner Model - Informações adicionais de parceiros
"""
from app import db
from datetime import datetime


class Partner(db.Model):
    """Informações adicionais de parceiros (motoristas, hotéis, quiosques)"""
    __tablename__ = 'partners'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Tipo de parceiro
    partner_type = db.Column(db.String(50), nullable=False)  # 'motorista', 'hotel', 'quiosque', 'agencia', 'outro'
    
    # Informações de negócio
    business_name = db.Column(db.String(200))  # Nome do negócio (se aplicável)
    description = db.Column(db.Text)  # Descrição dos serviços
    address = db.Column(db.String(500))
    
    # Documentação
    document_number = db.Column(db.String(50))  # CPF ou CNPJ
    license_number = db.Column(db.String(100))  # Número de licença/registro
    
    # Status de verificação
    verified = db.Column(db.Boolean, default=False)
    verification_date = db.Column(db.DateTime)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento
    user = db.relationship('User', foreign_keys=[user_id], backref='partner_info')
    
    def __repr__(self):
        return f'<Partner {self.partner_type} - User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'partner_type': self.partner_type,
            'business_name': self.business_name,
            'description': self.description,
            'address': self.address,
            'verified': self.verified,
            'verification_date': self.verification_date.isoformat() if self.verification_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
