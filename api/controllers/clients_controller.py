from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
from api.models.clients import Client
from api.models.db import db
from functools import wraps
from app.routes.login import current_user

client_bp = Blueprint('clients', __name__, url_prefix='/api')

# Decorator para verificar se o usuário está autenticado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Rota para obter todos os clientes
@client_bp.route('/clients', methods=['GET'])
@login_required
def get_clients():
    clients = Client.query.all()
    return jsonify([{'id': client.id, 'chat_id': client.chat_id, 'phone_number': client.phone_number, 'name': client.name, 'city': client.city, 'address': client.address} for client in clients])

# Rota para obter um cliente específico
@client_bp.route('/clients/<int:id>', methods=['GET'])
@login_required
def get_client(id):
    client = Client.query.get(id)
    if not client:
        return abort(404, 'Client not found')
    return jsonify({'id': client.id, 'chat_id': client.chat_id, 'phone_number': client.phone_number, 'name': client.name, 'city': client.city, 'address': client.address})

# Rota para criar um novo cliente
@client_bp.route('/clients', methods=['POST'])
@login_required
def create_client():
    if request.method == 'POST':
        name = request.form.get('name')
        chat_id = request.form.get('chat_id')
        phone_number = request.form.get('phone_number')
        city = request.form.get('city')
        address = request.form.get('address')

        if not name:
            return jsonify({'error': 'Name is required'}), 400

        new_client = Client(
            name=name,
            chat_id=chat_id,
            phone_number=phone_number,
            city=city,
            address=address
        )

        db.session.add(new_client)
        db.session.commit()

        # Retorna uma resposta JSON com status 200 e URL para redirecionamento
        return jsonify({'message': 'Cliente adicionado com sucesso', 'redirect': '/clientes'}), 200

# Rota para deletar um cliente
@client_bp.route('/clients/<int:id>', methods=['DELETE'])
@login_required
def delete_client(id):
    client = Client.query.get(id)
    if not client:
        return abort(404, 'Client not found')
    
    db.session.delete(client)
    db.session.commit()
    
    return jsonify({'message': 'Client deleted'})

@client_bp.route('/clients/<int:id>', methods=['PUT'])
@login_required
def update_client(id):
    client = Client.query.get(id)
    if not client:
        return abort(404, 'Client not found')
    
    # Atualiza os dados do cliente com os valores do formulário
    data = request.form
    client.name = data.get('name', client.name)
    client.chat_id = data.get('chat_id', client.chat_id)
    client.phone_number = data.get('phone_number', client.phone_number)
    client.city = data.get('city', client.city)
    client.address = data.get('address', client.address)
    db.session.commit()
    return jsonify({'message': 'Cliente atualizado com sucesso'}), 200