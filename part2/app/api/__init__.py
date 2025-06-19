from flask_restx import Api
from flask import Blueprint

# Import du namespace users
from app.api.v1.users import api as users_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(blueprint,
          version='1.0',
          title='HBnB API',
          description='HBnB Application API')

api.add_namespace(users_ns, path='/users')
