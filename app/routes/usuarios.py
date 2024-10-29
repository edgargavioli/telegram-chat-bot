from flask import Blueprint, render_template

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.route('/')
def usuarios():
    return render_template('pages/usuarios.html')
