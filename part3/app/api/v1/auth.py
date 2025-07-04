from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('auth', description='Authentication operations')

# Modèle d'entrée pour le login
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

facade = HBnBFacade()


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'JWT token returned')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authentifier l'utilisateur et renvoyer un jeton JWT"""
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })

        return {'access_token': access_token}, 200

    @api.route('/protected')
    class Protected(Resource):
        @jwt_required()
        @api.response(200, 'Access granted')
        @api.response(401, 'Missing or invalid token')
        def get(self):
            """Un point de terminaison protégé nécessitant une authentification JWT"""
            user = get_jwt_identity()
            return {'message': f"Hello, user {user['id']}"}, 200
