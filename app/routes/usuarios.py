from flask import Blueprint, render_template, flash, redirect, url_for
from . import login
from api.models.users import User

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.route('/')
def usuarios():
    if login.current_user.is_authenticated:
        return render_template('pages/usuarios/usuarios.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/adicionar')
def adicionar_usuario():
    if login.current_user.is_authenticated:
        return render_template('pages/usuarios/adicionar_usuario.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/editar/<int:id>')
def editar_usuario(id):
    if login.current_user.is_authenticated:
        user = User.query.get_or_404(id)
        return render_template('pages/usuarios/editar_usuario.html', user=user)
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))