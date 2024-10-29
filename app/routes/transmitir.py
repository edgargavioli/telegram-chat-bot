from flask import Blueprint, render_template

bp = Blueprint('transmitir', __name__, url_prefix='/transmitir')

@bp.route('/')
def transmitir():
    return render_template('pages/transmitir.html')
