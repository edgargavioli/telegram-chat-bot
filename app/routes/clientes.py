from flask import Blueprint, render_template, flash, redirect, url_for
from . import login
from api.models.clients import Client

bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@bp.route('/')
def clientes():
    if login.current_user.is_authenticated:
        return render_template('pages/clientes/clientes.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/adicionar')
def adicionar_cliente():
    if login.current_user.is_authenticated:
        return render_template('pages/clientes/adicionar_cliente.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/editar/<int:id>')
def editar_cliente(id):
    if login.current_user.is_authenticated:
        client = Client.query.get_or_404(id)
        return render_template('pages/clientes/editar_cliente.html', client=client)
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))