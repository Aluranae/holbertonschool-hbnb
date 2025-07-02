from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from .extensions import db, jwt

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns

# Instanciation de bcrypt en dehors de create_app
bcrypt = Bcrypt()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation de bcrypt avec l'app
    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Placeholder pour les namespaces de l'API (les endpoints seront ajoutés plus tard)
    # Les namespaces supplémentaires pour places, reviews et amenities seront ajoutés ultérieurement

    return app
