from flask import Flask
from config import DevelopmentConfig
from .extensions import db, jwt

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)
    jwt.init_app(app)


    return app
