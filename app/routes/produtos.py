from flask import Blueprint, render_template, flash, redirect, url_for
from . import login
from api.models.products import Product

bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@bp.route('/')
def produtos():
    if login.current_user.is_authenticated:
        return render_template('pages/produtos/produtos.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/adicionar')
def adicionar_produto():
    if login.current_user.is_authenticated:
        return render_template('pages/produtos/adicionar_produto.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/editar/<int:id>')
def editar_produto(id):
    if login.current_user.is_authenticated:
        product = Product.query.get_or_404(id)
        return render_template('pages/produtos/editar_produto.html', product=product)
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))