from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
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
        'role': user.role
    })

@user_bp.route('/users', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        if name and username and password and role:
            new_user = User(
                name=name,
                username=username,
                password=generate_password_hash(password),
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('usuarios.usuarios'))
        else:
            pass
    return render_template('pages/usuarios/adicionar_usuario.html')

@user_bp.route('/users/<int:id>', methods=['POST', 'PUT'])
@login_required
def update_user(id):
    user = User.query.get_or_404(id)
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    if name and username and password and role:
        user.name = name
        user.username = username
        user.password = generate_password_hash(password)
        user.role = role
        db.session.commit()
        return redirect(url_for('usuarios.usuarios'))
    else:
        pass

@user_bp.route('/users/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return abort(404, 'User not found')
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})