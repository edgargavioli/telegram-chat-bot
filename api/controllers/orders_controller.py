from flask import Blueprint, jsonify, request, abort
from api.models.orders import Order
from api.models.db import db
from functools import wraps
from app.routes.login import current_user

order_bp = Blueprint('orders', __name__, url_prefix='/api')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@order_bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': order.id,
        'created_date': order.created_date,
        'status': order.status,
        'amount': order.amount,
        'client_id': order.client_id,
        'client': {
            'id': order.client.id,
            'chat_id': order.client.chat_id,
            'phone_number': order.client.phone_number,
            'name': order.client.name,
            'city': order.client.city,
            'address': order.client.address
        } if order.client else None
    } for order in orders])

@order_bp.route('/orders/<int:id>', methods=['GET'])
@login_required
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return abort(404, 'Order not found')
    return jsonify({
        'id': order.id,
        'created_date': order.created_date,
        'status': order.status,
        'amount': order.amount,
        'client_id': order.client_id,
        'client': {
            'id': order.client.id,
            'chat_id': order.client.chat_id,
            'phone_number': order.client.phone_number,
            'name': order.client.name,
            'city': order.client.city,
            'address': order.client.address
        } if order.client else None
    })

@order_bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.get_json()
    new_order = Order(
        created_date=data['created_date'],
        status=data['status'],
        amount=data['amount'],
        client_id=data['client_id']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({
        'id': new_order.id,
        'created_date': new_order.created_date,
        'status': new_order.status,
        'amount': new_order.amount,
        'client_id': new_order.client_id
    }), 201

@order_bp.route('/orders/<int:id>', methods=['PUT'])
@login_required
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return abort(404, 'Order not found')
    data = request.get_json()
    order.created_date = data['created_date']
    order.status = data['status']
    order.amount = data['amount']
    order.client_id = data['client_id']
    db.session.commit()
    return jsonify({
        'id': order.id,
        'created_date': order.created_date,
        'status': order.status,
        'amount': order.amount,
        'client_id': order.client_id
    })

@order_bp.route('/orders/<int:id>', methods=['DELETE'])
@login_required
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return abort(404, 'Order not found')
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'})
