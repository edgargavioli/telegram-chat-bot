from .db import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=False)
    photo_url = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False, unique=False)
    description = db.Column(db.String(255), nullable=False, unique=False)
    price = db.Column(db.Numeric(10, 2), nullable=False, unique=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, unique=False)
    category = db.relationship('Category', backref='products')

    def __repr__(self):
        return f'<Product {self.name}>'