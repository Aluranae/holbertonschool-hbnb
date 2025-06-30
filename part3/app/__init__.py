from flask import Flask
from config import DevelopmentConfig
from .extensions import db, jwt

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialise les extensions
    db.init_app(app)
    jwt.init_app(app)

    # Import et registre les blueprints ici si nécessaire
    # from .routes.main import main_bp
    # app.register_blueprint(main_bp)

    return app
