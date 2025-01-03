from flask import Blueprint, render_template, flash, redirect, url_for
from . import login

bp = Blueprint('mensagens', __name__, url_prefix='/mensagens')

@bp.route('/')
def mensagens():
    if login.current_user.is_authenticated:
        return render_template('pages/mensagens/mensagens.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))
