from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
from api.models.clients import Client
from api.models.db import db
from functools import wraps
from app.routes.login import current_user

client_bp = Blueprint('clients', __name__, url_prefix='/api')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@client_bp.route('/clients', methods=['GET'])
@login_required
def get_clients():
    clients = Client.query.all()
    return jsonify([{'id': client.id, 'chat_id': client.chat_id, 'phone_number': client.phone_number, 'name': client.name, 'city': client.city, 'address': client.address, 'is_active': client.is_active} for client in clients])

@client_bp.route('/clients/<int:id>', methods=['GET'])
@login_required
def get_client(id):
    client = Client.query.get(id)
    if not client:
        return abort(404, 'Client not found')
    return jsonify({'id': client.id, 'chat_id': client.chat_id, 'phone_number': client.phone_number, 'name': client.name, 'city': client.city, 'address': client.address, 'is_active': client.is_active})

@client_bp.route('/clients', methods=['GET', 'POST'])
@login_required
def create_client():
    if request.method == 'POST':
        chat_id = request.form.get('chat_id')
        phone_number = request.form.get('phone_number')
        name = request.form.get('name')
        city = request.form.get('city')
        address = request.form.get('address')
        is_active = int(request.form.get('is_active'))
        if chat_id and phone_number and name and city and address:
            new_client = Client(
                chat_id=chat_id,
                phone_number=phone_number,
                name=name,
                city=city,
                address=address,
                is_active=is_active
            )
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('clientes.clientes'))
        else:
            pass
    return render_template('pages/clientes/adicionar_cliente.html')


@client_bp.route('/clients/<int:id>', methods=['POST', 'PUT'])
@login_required
def update_client(id):
    client = Client.query.get_or_404(id)
    chat_id = request.form.get('chat_id')
    phone_number = request.form.get('phone_number')
    name = request.form.get('name')
    city = request.form.get('city')
    address = request.form.get('address')
    is_active = int(request.form.get('is_active'))
    if chat_id and phone_number and name and city and address:
        client.chat_id = chat_id
        client.phone_number = phone_number
        client.name = name
        client.city = city
        client.address = address
        client.is_active = is_active
        db.session.commit()
        return redirect(url_for('clientes.clientes'))
    else:
        pass

@client_bp.route('/clients/<int:id>', methods=['DELETE'])
@login_required
def delete_client(id):
    client = Client.query.get(id)
    if not client:
        return abort(404, 'Client not found')
    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted'})