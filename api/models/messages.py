from .db import db

class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('clients.chat_id'), nullable=False, unique=False)
    client = db.relationship('Client', backref='messages')
    message = db.Column(db.String(500), nullable=False, unique=False)
    type = db.Column(db.String(50), nullable=False, default='received')

    def __repr__(self):
        return f'<Messages chat_id={self.chat_id} message={self.message}>'