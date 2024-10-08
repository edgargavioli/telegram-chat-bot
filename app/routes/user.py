from flask import Blueprint, render_template, jsonify

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/')
def user_list():
    return jsonify({"users": ["user1", "user2", "user3"]})

@bp.route('/greet')
def greet():
    return render_template('index.html')
