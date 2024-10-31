from flask import Blueprint, jsonify, request, abort
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
    return jsonify([{'id': client.id, 'chat_id': client.chat_id, 'phone_number': client.phone_number, 'name': client.name, 'city': client.city, 'address': client.address} for client in clients])

@client_bp.route('/clients/<int:id>', methods=['GET'])
@login_required
def get_client(id):
    client = Client.query.get(id)
    if not client:
        return abort(404, 'Client not found')
    return jsonify({'id': client.id, 'chat_id': client.chat_id, 'phone_number': client.phone_number, 'name': client.name, 'city': client.city, 'address': client.address})

@client_bp.route('/clients', methods=['POST'])
@login_required
def create_client():
    data = request.get_json()
    new_client = Client(
        chat_id=data['chat_id'],
        phone_number=data['phone_number'],
        name=data['name'],
        city=data['city'],
        address=data['address']
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'id': new_client.id, 'chat_id': new_client.chat_id, 'phone_number': new_client.phone_number, 'name': new_client.name, 'city': new_client.city, 'address': new_client.address}), 201

@client_bp.route('/clients/<int:id>', methods=['PUT'])
@login_required
def update_client(id):
    client = Client.query.get(id)
    if not client:
        return abort(404, 'Client not found')
    data = request.get_json()
    client.chat_id = data['chat_id']
    client.phone_number = data['phone_number']
    client.name = data['name']
    client.city = data['city']
    client.address = data['address']
    db.session.commit()
    return jsonify({'id': client.id, 'chat_id': client.chat_id, 'phone_number': client.phone_number, 'name': client.name, 'city': client.city, 'address': client.address})

@client_bp.route('/clients/<int:id>', methods=['DELETE'])
@login_required
def delete_client(id):
    client = Client.query.get(id)
    if not client:
        return abort(404, 'Client not found')
    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted'})