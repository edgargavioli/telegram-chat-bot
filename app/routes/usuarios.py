from flask import Blueprint, render_template, flash, redirect, url_for
from . import login

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.route('/')
def usuarios():
    if login.current_user.is_authenticated:
        return render_template('pages/usuarios.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))
