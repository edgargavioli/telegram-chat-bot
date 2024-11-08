from flask import Blueprint, render_template, flash, redirect, url_for
from . import login

bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@bp.route('/')
def pedidos():
    if login.current_user.is_authenticated:
        return render_template('pages/orders/pedidos.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))
