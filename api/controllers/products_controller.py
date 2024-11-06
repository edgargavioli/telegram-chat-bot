from flask import Blueprint, current_app, jsonify, redirect, render_template, request, abort, url_for
from api.models.products import Product
from api.models.db import db
from functools import wraps
from app.routes.login import current_user
from werkzeug.utils import secure_filename
import os

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

@product_bp.route('/products', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        
        photo_file = request.files.get('photo')
        if photo_file:
            filename = secure_filename(photo_file.filename)
            photo_file.save(f'app/static/img/produtos/{filename}')
        else:
            pass
        if name and description and price and category_id:
            new_product = Product(
                name=name,
                photo_url=filename,
                description=description,
                price=float(price),
                category_id=int(category_id)
            )
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('produtos.produtos'))
        else:
            pass
    return render_template('pages/produtos/adicionar_produto.html')

@product_bp.route('/products/<int:id>', methods=['POST', 'PUT'])
@login_required
def update_product(id):
    product = Product.query.get(id)
    product.name = request.form['name']
    product.description = request.form['description']
    product.price = request.form['price']
    product.category_id = request.form['category_id']
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            photo.save(f'app/static/img/produtos/{filename}')
            os.remove(f'app/static/img/produtos/{product.photo_url}')
            product.photo_url = filename
    db.session.commit()
    return redirect(url_for('produtos.produtos'))

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return abort(404, 'Product not found')
    os.remove(f'app/static/img/produtos/{product.photo_url}')
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})
