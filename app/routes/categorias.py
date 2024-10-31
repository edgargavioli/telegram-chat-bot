from flask import Blueprint, render_template, flash, redirect, url_for
from . import login

bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@bp.route('/')
def categorias():
    if login.current_user.is_authenticated:
        return render_template('pages/categorias.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))
