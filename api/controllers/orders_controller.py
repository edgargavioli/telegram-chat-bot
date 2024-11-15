from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
from api.models.orders import Order
from api.models.db import db
from api.models.clients import Client
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
    if request.method == 'POST':
        created_date = request.form.get('created_date')
        created_time = request.form.get('created_time')
        status = request.form.get('status')
        amount = request.form.get('amount')
        client_id = request.form.get('client_id')
        created_date_time = f'{created_date} {created_time}'
        if created_date_time and status and amount and client_id:
            new_order = Order(
                created_date=created_date_time,
                status=status,
                amount=amount,
                client_id=client_id
            )
            db.session.add(new_order)
            db.session.commit()
            return redirect(url_for('pedidos.pedidos'))
        else:
            pass
    return render_template('pages/pedidos/adicionar_pedido.html')

@order_bp.route('/orders/bot<int:chat_id>', methods=['POST'])
def create_order_bot(chat_id):
    if request.method == 'POST':
        data = request.get_json()

        created_date = data.get('created_date')
        created_time = data.get('created_time')
        status = data.get('status')
        amount = data.get('amount')

        client = Client.query.filter_by(chat_id=chat_id).first()
        
        if not client:
            return jsonify({'message': 'Cliente não encontrado'}), 404

        client_id = client.id

        created_date_time = f'{created_date} {created_time}' if created_date and created_time else None

        if created_date_time and status and amount and client_id:
            new_order = Order(
                created_date=created_date_time,
                status=status,
                amount=amount,
                client_id=client_id
            )
            db.session.add(new_order)
            db.session.commit()

            return jsonify({'Order': new_order.to_dict()}), 200
        else:
            return jsonify({'message': 'Campos obrigatórios faltando'}), 400

@order_bp.route('/orders/<int:id>', methods=['POST', 'PUT'])
@login_required
def update_order(id):
    order = Order.query.get(id)
    new_date = request.form.get('saved_date')
    new_time = request.form.get('saved_time')
    order.created_date = f'{new_date} {new_time}'
    order.status = request.form.get('status')
    order.amount = request.form.get('amount')
    order.client_id = request.form.get('client_id')
    if order.created_date and order.status and order.amount and order.client_id:
        db.session.commit()
    return redirect(url_for('pedidos.pedidos'))

@order_bp.route('/orders/<int:id>', methods=['DELETE'])
@login_required
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return abort(404, 'Order not found')
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'})