from flask import Blueprint, render_template, flash, redirect, request, url_for
from . import login
from api.models.categories import Category

bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@bp.route('/')
def categorias():
    if login.current_user.is_authenticated:
        return render_template('pages/categorias/categorias.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/adicionar')
def adicionar_categoria():
    if login.current_user.is_authenticated:
        return render_template('pages/categorias/adicionar_categoria.html')
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))

@bp.route('/editar/<int:id>')
def editar_categoria(id):
    if login.current_user.is_authenticated:
        category = Category.query.get_or_404(id)
        return render_template('pages/categorias/editar_categoria.html', category=category)
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login.login'))