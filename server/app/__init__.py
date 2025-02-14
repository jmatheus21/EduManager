from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensões
    db.init_app(app)

    # Registra rotas
    from .routes import init_routes
    init_routes(app)

    return app