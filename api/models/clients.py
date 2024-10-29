from .db import db

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=False)
    name = db.Column(db.String(120), nullable=False, unique=False)
    city = db.Column(db.String(255), nullable=False, unique=False)
    address = db.Column(db.String(255), nullable=False, unique=False)

    def __repr__(self):
        return f'<Client {self.name}>'