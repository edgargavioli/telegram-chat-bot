from flask import Blueprint, render_template

bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@bp.route('/')
def clientes():
    return render_template('pages/clientes.html')
