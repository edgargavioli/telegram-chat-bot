from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone
from api.models.user import User

bp = Blueprint('login', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated and request.cookies.get('login_time'):
        return redirect(url_for('home.home'))
    else:
        logout_user()
        return redirect(url_for('login.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and request.cookies.get('login_time'):
        return redirect(url_for('home.home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = 'save-session' in request.form

        print(generate_password_hash(password))

        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            
            response = make_response(redirect(url_for('home.home')))
            login_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            
            if remember_me:
                response.set_cookie('login_time', login_time, max_age=86400, secure=True, httponly=True, samesite='Strict')
            else:
                response.set_cookie('login_time', '', expires=0)
            
            return response
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
            return redirect(url_for('login.login'))
    return render_template('pages/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login.login'))
