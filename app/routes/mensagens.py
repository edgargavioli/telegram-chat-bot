from flask import Blueprint, render_template

bp = Blueprint('mensagens', __name__, url_prefix='/mensagens')

@bp.route('/')
def mensagens():
    return render_template('pages/mensagens.html')
