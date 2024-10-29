from flask import Blueprint, render_template

bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@bp.route('/')
def produtos():
    return render_template('pages/produtos.html')
