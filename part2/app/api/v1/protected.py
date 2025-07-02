from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('protected', description='Protected routes')

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user["id"]}'}, 200
