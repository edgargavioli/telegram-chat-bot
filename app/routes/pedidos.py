from flask import Blueprint, render_template, flash, redirect, url_for
from . import login
from api.models.orders import Order
from api.models.products import Product

bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@bp.route('/')
def pedidos():
    if login.current_user.is_authenticated:
        return render_template('pages/pedidos/pedidos.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/adicionar')
def adicionar_pedido():
    if login.current_user.is_authenticated:
        return render_template('pages/pedidos/adicionar_pedido.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/editar/<int:id>')
def editar_pedido(id):
    if login.current_user.is_authenticated:
        order = Order.query.get_or_404(id)
        saved_date, saved_time = str(order.created_date).split(' ')
        all_products = Product.query.all()
        return render_template('pages/pedidos/editar_pedido.html', order=order, saved_date=saved_date, saved_time=saved_time, all_products=all_products)
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))