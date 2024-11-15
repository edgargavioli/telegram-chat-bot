from flask import Flask, request, redirect, url_for, flash
from api.controllers import categories_controller
from api.controllers import clients_controller
from api.controllers import orders_controller
from api.controllers import orders_items_controller
from api.controllers import products_controller
from api.controllers import user_controller
from api.controllers import messages_controller
from .routes.login import bp as login_bp
from .routes.home import bp as home_bp
from .routes.categorias import bp as categorias_bp
from .routes.clientes import bp as clientes_bp
from .routes.mensagens import bp as mensagens_bp
from .routes.pedidos import bp as pedidos_bp
from .routes.produtos import bp as produtos_bp
from .routes.transmitir import bp as transmitir_bp
from .routes.usuarios import bp as usuarios_bp
from .config import Config
from flask_migrate import Migrate
from api.models.db import db
from api.models.users import User
from api.models.categories import Category
from api.models.products import Product
from api.models.orders import Order
from api.models.clients import Client
from api.models.orders_items import OrderItems
from flask_login import LoginManager, current_user, logout_user
from datetime import datetime, timezone

migrate = Migrate()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    login_manager.login_message = 'Por Favor, faça login para acessar esta página!'

    # Inicializa o banco de dados
    db.init_app(app)

    # Configura o migrations
    migrate.init_app(app, db, directory='./migrations')

    # Registrar Blueprints
    app.register_blueprint(categories_controller.category_bp)
    app.register_blueprint(clients_controller.client_bp)
    app.register_blueprint(orders_controller.order_bp)
    app.register_blueprint(orders_items_controller.order_items_bp)
    app.register_blueprint(products_controller.product_bp)
    app.register_blueprint(user_controller.user_bp)
    app.register_blueprint(messages_controller.messages_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(mensagens_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(transmitir_bp)
    app.register_blueprint(usuarios_bp)

    @app.before_request
    def check_session_expiration():
        if current_user.is_authenticated:
            login_time_cookie = request.cookies.get('login_time')
            if login_time_cookie:
                login_time = datetime.strptime(login_time_cookie, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                elapsed_time = datetime.now(timezone.utc) - login_time
                session_lifetime = app.permanent_session_lifetime
                if elapsed_time > session_lifetime:
                    logout_user()
                    flash('Sua sessão expirou. Faça login novamente.', 'warning')
                    return redirect(url_for('login.login'))
            
    @app.context_processor
    def inject_user():
        return dict(username=current_user.username if current_user.is_authenticated else None)

    with app.app_context():
        db.create_all()

    return app