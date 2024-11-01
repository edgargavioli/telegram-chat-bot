from .db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=False)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False, unique=False)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(120), nullable=False, unique=False)

    def __repr__(self):
        return f'<User {self.username}>'