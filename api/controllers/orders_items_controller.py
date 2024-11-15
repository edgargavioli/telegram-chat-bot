from flask import Blueprint, jsonify, request, abort
from api.models.orders_items import OrderItems
from api.models.db import db
from functools import wraps
from app.routes.login import current_user

order_items_bp = Blueprint('orders_items', __name__, url_prefix='/api')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@order_items_bp.route('/orders_items', methods=['GET'])
@login_required
def get_orders_items():
    orders_items = OrderItems.query.all()
    return jsonify([{
        'id': order_item.id,
        'order_id': order_item.order_id,
        'order': {
            'id': order_item.order.id,
            'created_date': order_item.order.created_date,
            'status': order_item.order.status,
            'amount': order_item.order.amount,
            'client_id': order_item.order.client_id,
            'client': {
                'id': order_item.order.client.id,
                'chat_id': order_item.order.client.chat_id,
                'phone_number': order_item.order.client.phone_number,
                'name': order_item.order.client.name,
                'city': order_item.order.client.city,
                'address': order_item.order.client.address
            } if order_item.order.client else None
        } if order_item.order else None,
        'product_id': order_item.product_id,
        'product': {
            'id': order_item.product.id,
            'name': order_item.product.name,
            'photo_url': order_item.product.photo_url,
            'description': order_item.product.description,
            'price': order_item.product.price,
            'category_id': order_item.product.category_id,
            'category': {
                'id': order_item.product.category.id,
                'name': order_item.product.category.name
            } if order_item.product.category else None
        } if order_item.product else None,
        'quantity': order_item.quantity,
        'product_price': order_item.product_price,
        'product_name': order_item.product_name
    } for order_item in orders_items])

@order_items_bp.route('/orders_items/<int:id>', methods=['GET'])
@login_required
def get_order_item(id):
    order_item = OrderItems.query.get(id)
    if not order_item:
        return abort(404, 'Order item not found')
    return jsonify({
        'id': order_item.id,
        'order_id': order_item.order_id,
        'order': {
            'id': order_item.order.id,
            'created_date': order_item.order.created_date,
            'status': order_item.order.status,
            'amount': order_item.order.amount,
            'client_id': order_item.order.client_id,
            'client': {
                'id': order_item.order.client.id,
                'chat_id': order_item.order.client.chat_id,
                'phone_number': order_item.order.client.phone_number,
                'name': order_item.order.client.name,
                'city': order_item.order.client.city,
                'address': order_item.order.client.address
            } if order_item.order.client else None
        } if order_item.order else None,
        'product_id': order_item.product_id,
        'product': {
            'id': order_item.product.id,
            'name': order_item.product.name,
            'photo_url': order_item.product.photo_url,
            'description': order_item.product.description,
            'price': order_item.product.price,
            'category_id': order_item.product.category_id,
            'category': {
                'id': order_item.product.category.id,
                'name': order_item.product.category.name
            } if order_item.product.category else None
        } if order_item.product else None,
        'quantity': order_item.quantity,
        'product_price': order_item.product_price,
        'product_name': order_item.product_name
    })

@order_items_bp.route('/orders_items', methods=['POST'])
def create_order_item():
    data = request.get_json()
    new_order_item = OrderItems(
        order_id=data['order_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        product_price=data['product_price'],
        product_name=data['product_name']
    )
    db.session.add(new_order_item)
    db.session.commit()
    return jsonify({
        'id': new_order_item.id,
        'order_id': new_order_item.order_id,
        'product_id': new_order_item.product_id,
        'quantity': new_order_item.quantity,
        'product_price': new_order_item.product_price,
        'product_name': new_order_item.product_name
    }), 201

@order_items_bp.route('/orders_items/<int:id>', methods=['PUT'])
@login_required
def update_order_item(id):
    order_item = OrderItems.query.get(id)
    if not order_item:
        return abort(404, 'Order item not found')
    data = request.get_json()
    order_item.order_id = data['order_id']
    order_item.product_id = data['product_id']
    order_item.quantity = data['quantity']
    order_item.product_price = data['product_price']
    order_item.product_name = data['product_name']
    db.session.commit()
    return jsonify({
        'id': order_item.id,
        'order_id': order_item.order_id,
        'product_id': order_item.product_id,
        'quantity': order_item.quantity,
        'product_price': order_item.product_price,
        'product_name': order_item.product_name
    })

@order_items_bp.route('/orders_items/<int:id>', methods=['DELETE'])
@login_required
def delete_order_item(id):
    order_item = OrderItems.query.get(id)
    if not order_item:
        return abort(404, 'Order item not found')
    db.session.delete(order_item)
    db.session.commit()
    return jsonify({'message': 'Order item deleted'})
