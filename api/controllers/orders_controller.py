from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
from api.models.orders import Order
from api.models.db import db
from api.models.clients import Client
from functools import wraps
from app.routes.login import current_user
from api.models.products import Product
from api.models.orders_items import OrderItems

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
        products = request.form.getlist('products[]')
        quantities = request.form.getlist('quantities[]')
        created_date_time = f'{created_date} {created_time}'
        if created_date_time and status and amount and client_id and products and quantities:
            new_order = Order(
                created_date=created_date_time,
                status=status,
                amount=amount,
                client_id=client_id
            )
            db.session.add(new_order)
            db.session.commit()
            for product_id, quantity in zip(products, quantities):
                product = Product.query.get(product_id)
                if product:
                    order_item = OrderItems(
                        order_id=new_order.id,
                        product_id=product.id,
                        quantity=int(quantity),
                        product_price=product.price,
                        product_name=product.name
                    )
                    db.session.add(order_item)
            db.session.commit()
            return redirect(url_for('pedidos.pedidos'))
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
    if not order:
        return abort(404, 'Pedido não encontrado')
    new_date = request.form.get('saved_date')
    new_time = request.form.get('saved_time')
    order.created_date = f'{new_date} {new_time}'
    order.status = request.form.get('status')
    order.amount = request.form.get('amount')
    order.client_id = request.form.get('client_id')
    if order.created_date and order.status and order.client_id:
        order_items = OrderItems.query.filter_by(order_id=order.id).all()
        for item in order_items:
            db.session.delete(item)
        product_ids = request.form.getlist('products[]')
        product_quantities = request.form.getlist('quantities[]')
        for product_id, quantity in zip(product_ids, product_quantities):
            product = Product.query.get(product_id)
            if product:
                order_item = OrderItems(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=int(quantity),
                    product_price=product.price,
                    product_name=product.name
                )
                db.session.add(order_item)
        db.session.commit()
    return redirect(url_for('pedidos.pedidos'))

@order_bp.route('/orders/status/<int:id>', methods=['POST'])
@login_required
def update_order_status(id):
    data = request.json
    new_status = data.get('status')
    if not new_status:
        return jsonify({"error": "Status is required"}), 400
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    order.status = new_status
    if new_status == "Concluído":
        order_items = OrderItems.query.filter_by(order_id=order.id).all()
        for item in order_items:
            db.session.delete(item)
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order completed and deleted successfully"}), 200
    db.session.commit()
    return jsonify({"message": "Order status updated successfully"}), 200

@order_bp.route('/orders/<int:id>', methods=['DELETE'])
@login_required
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return abort(404, 'Pedido não encontrado')
    order_items = OrderItems.query.filter_by(order_id=order.id).all()
    for item in order_items:
        db.session.delete(item)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Pedido e itens associados excluídos com sucesso'})
