from flask import Flask
from .routes.user import bp as user_bp
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
    app.register_blueprint(user_bp)

    return app
