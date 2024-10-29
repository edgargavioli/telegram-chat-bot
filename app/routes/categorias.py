from flask import Blueprint, render_template

bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@bp.route('/')
def categorias():
    return render_template('pages/categorias.html')
