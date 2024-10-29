from .db import db

class OrderItems(db.Model):
    __tablename__ = 'orders_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=False)
    order = db.relationship('Order', backref='orders_items')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, unique=False)
    product = db.relationship('Product', backref='orders_items')
    quantity = db.Column(db.Integer, nullable=False, unique=False)
    product_price = db.Column(db.Numeric(10, 2), nullable=False, unique=False)
    product_name = db.Column(db.String(120), nullable=False, unique=False)

    def __repr__(self):
        return f'<OrderItems {self.product_name}>'