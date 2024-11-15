from .db import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False, unique=False)
    status = db.Column(db.String(120), nullable=False, unique=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False, unique=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False, unique=False)
    client = db.relationship('Client', backref='orders')

    def to_dict(self):
        return {
            'id': self.id,
            'created_date': self.created_date,
            'status': self.status,
            'amount': self.amount,
            'client_id': self.client_id
        }

    def __repr__(self):
        return f'<Order {self.status}>'