from flask import Blueprint, jsonify, request, abort
from api.models.products import Product
from api.models.db import db
from functools import wraps
from app.routes.login import current_user

product_bp = Blueprint('products', __name__, url_prefix='/api')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@product_bp.route('/products', methods=['GET'])
@login_required
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'photo_url': product.photo_url,
        'description': product.description,
        'price': product.price,
        'category_id': product.category_id,
        'category': {
            'id': product.category.id,
            'name': product.category.name
        } if product.category else None
    } for product in products])

@product_bp.route('/products/<int:id>', methods=['GET'])
@login_required
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return abort(404, 'Product not found')
    return jsonify({
        'id': product.id,
        'name': product.name,
        'photo_url': product.photo_url,
        'description': product.description,
        'price': product.price,
        'category_id': product.category_id,
        'category': {
            'id': product.category.id,
            'name': product.category.name
        } if product.category else None
    })

@product_bp.route('/products', methods=['POST'])
@login_required
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        photo_url=data['photo_url'],
        description=data['description'],
        price=data['price'],
        category_id=data['category_id']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({
        'id': new_product.id,
        'name': new_product.name,
        'photo_url': new_product.photo_url,
        'description': new_product.description,
        'price': new_product.price,
        'category_id': new_product.category_id,
        'category': {
            'id': new_product.category.id,
            'name': new_product.category.name
        } if new_product.category else None
    }), 201

@product_bp.route('/products/<int:id>', methods=['PUT'])
@login_required
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return abort(404, 'Product not found')
    data = request.get_json()
    product.name = data['name']
    product.photo_url = data['photo_url']
    product.description = data['description']
    product.price = data['price']
    product.category_id = data['category_id']
    db.session.commit()
    return jsonify({
        'id': product.id,
        'name': product.name,
        'photo_url': product.photo_url,
        'description': product.description,
        'price': product.price,
        'category_id': product.category_id,
        'category': {
            'id': product.category.id,
            'name': product.category.name
        } if product.category else None
    })

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return abort(404, 'Product not found')
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})
