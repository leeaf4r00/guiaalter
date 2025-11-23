"""
Tour Models - ORM SQLAlchemy
"""
from app import db

class Tour(db.Model):
    """Modelo de passeio turístico"""
    __tablename__ = 'tours'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False, index=True) # e.g., 'rioarapiuns', 'lagoverde'
    whatsapp_message = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Tour {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'whatsapp_message': self.whatsapp_message,
            'is_active': self.is_active
        }
