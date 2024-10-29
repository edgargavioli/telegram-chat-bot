from flask import Blueprint, render_template

bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@bp.route('/')
def pedidos():
    return render_template('pages/pedidos.html')
