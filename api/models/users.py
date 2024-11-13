from .db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=False)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False, unique=False)
    role = db.Column(db.String(120), nullable=False, unique=False)

    def __repr__(self):
        return f'<User {self.username}>'