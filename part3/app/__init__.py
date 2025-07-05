from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Configuration par défaut
from config import DevelopmentConfig

# Extensions initialisées dans un fichier séparé
from .extensions import db, jwt

# Import des namespaces API
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

# Instanciation manuelle de bcrypt (conforme à ta structure)
bcrypt = Bcrypt()


def create_app(config_class=DevelopmentConfig):
    # Création de l'application Flask
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Désactive les warnings inutiles de SQLAlchemy (si pas déjà dans config.py)
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    # Initialisation des extensions
    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    # Définition de l'API avec Swagger + auth JWT
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        security='Bearer Auth',
        authorizations={
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
            }
        }
    )

    # Enregistrement des namespaces (endpoints)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
