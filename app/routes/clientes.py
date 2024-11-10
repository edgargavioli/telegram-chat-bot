from flask import Blueprint, render_template, flash, redirect, url_for, request

from api.models import db
from api.models.clients import Client
from . import login
from . import clientes  # Modelo Client


bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@bp.route('/')
def clientes():
    if login.current_user.is_authenticated:
        clientes= Client.query.all()
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

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if not login.current_user.is_authenticated:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

    cliente = Client.query.get(id)
    if not cliente:
        flash('Cliente não encontrado.', 'danger')
        return redirect(url_for('clientes.clientes'))

    if request.method == 'POST':
        # Atualizar as informações do cliente com os dados do formulário
        cliente.chat_id = request.form['chat_id']
        cliente.name = request.form['name']
        cliente.phone_number = request.form['phone_number']
        cliente.city = request.form['city']
        cliente.address = request.form['address']

        db.session.commit()

        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('clientes.clientes'))

    # Para o método GET, exibir o formulário de edição preenchido com os dados do cliente
    return render_template('pages/clientes/editar_cliente.html', cliente=cliente)