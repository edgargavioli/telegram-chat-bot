from flask import Blueprint, jsonify, request, abort
from api.models.users import User
from api.models.db import db
from werkzeug.security import generate_password_hash
from functools import wraps
from app.routes.login import current_user

user_bp = Blueprint('users', __name__, url_prefix='/api')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'password': user.password,
        'is_active': user.is_active,
        'role': user.role
    } for user in users])

@user_bp.route('/users/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        return abort(404, 'User not found')
    return jsonify({
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'password': user.password,
        'is_active': user.is_active,
        'role': user.role
    })

@user_bp.route('/users', methods=['POST'])
@login_required
def create_user():
    data = request.get_json()
    new_user = User(
        name=data['name'],
        username=data['username'],
        password=generate_password_hash(data['password']),
        is_active=data['is_active'],
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'id': new_user.id,
        'name': new_user.name,
        'username': new_user.username,
        'password': new_user.password,
        'is_active': new_user.is_active,
        'role': new_user.role
    }), 201

@user_bp.route('/users/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    user = User.query.get(id)
    if not user:
        return abort(404, 'User not found')
    data = request.get_json()
    user.name = data['name']
    user.username = data['username']
    user.password = generate_password_hash(data['password'])
    user.is_active = data['is_active']
    user.role = data['role']
    db.session.commit()
    return jsonify({
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'password': user.password,
        'is_active': user.is_active,
        'role': user.role
    })

@user_bp.route('/users/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return abort(404, 'User not found')
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
