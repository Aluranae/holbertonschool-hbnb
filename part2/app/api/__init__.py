from flask_restx import Api
from flask import Blueprint

# Import du namespace amenities
from app.api.v1.amenities import api as amenities_ns

# Création d'un blueprint pour versionner l'API
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

# Création de l'objet Api avec le blueprint
api = Api(blueprint,
          title='HBnB API',
          version='1.0',
          description='API for HBnB application')

# Enregistrement du namespace amenities
api.add_namespace(amenities_ns, path='/amenities')
