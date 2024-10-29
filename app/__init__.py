from flask import Flask
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
from api.models.user import User
from api.models.categories import Category
from api.models.products import Product
from api.models.orders import Order
from api.models.clients import Client
from api.models.orders_items import OrderItems

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa o banco de dados
    db.init_app(app)

    # Configura o migrations
    migrate.init_app(app, db, directory='./migrations')

    # Registrar Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(mensagens_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(transmitir_bp)
    app.register_blueprint(usuarios_bp)

    return app
