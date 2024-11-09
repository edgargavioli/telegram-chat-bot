from flask import Blueprint, render_template, flash, redirect, url_for, request

from api.models import db
from api.models.clients import Client
from . import login
from . import clientes  # Modelo Client


bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@bp.route('/')
def clientes():
    if login.current_user.is_authenticated:
        return render_template('pages/clientes/clientes.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if login.current_user.is_authenticated:
        try:
            cliente = Client.query.get(id)  # Obtém o cliente pelo ID
            if cliente is None:
                flash('Cliente não encontrado!', 'danger')
                return redirect(url_for('clientes.clientes'))

            if request.method == 'POST':
                # Atualiza os campos do cliente com os novos valores do formulário
                cliente.chat_id = request.form['chat_id']
                cliente.name = request.form['name']
                cliente.phone_number = request.form['phone_number']
                cliente.city = request.form['city']
                cliente.address = request.form['address']

                # Salva as alterações no banco
                db.session.commit()

                flash('Cliente atualizado com sucesso!', 'success')
                return redirect(url_for('clientes.clientes'))  # Redireciona para a página de clientes

            # Renderiza o formulário de edição com os dados do cliente
            return render_template('pages/clientes/editar_cliente.html', cliente=cliente)
        
        except Exception as e:
            flash(f'Erro ao editar o cliente: {str(e)}', 'danger')
            return redirect(url_for('clientes.clientes'))
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
