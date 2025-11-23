from app import db
from datetime import datetime
import json

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    tour_name = db.Column(db.String(120), nullable=False)
    items_json = db.Column(db.Text, nullable=True)  # JSON string of cart items
    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reservation {self.id} - {self.tour_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tour_name': self.tour_name,
            'items': json.loads(self.items_json) if self.items_json else [],
            'total_price': float(self.total_price),
            'created_at': self.created_at.isoformat()
        }
