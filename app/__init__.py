from flask import Flask
from .routes.user import bp as user_bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrar Blueprints
    app.register_blueprint(user_bp)

    return app
