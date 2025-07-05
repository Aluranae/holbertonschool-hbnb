"""api/v1/auth.py

Définit les routes d'authentification pour l'application HBnB.
Comprend le point de terminaison /login pour la génération de jetons JWT,
et un exemple de route protégée par JWT (/protected).
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

# Création du namespace pour l'authentification
api = Namespace('auth', description='Authentication operations')

# Modèle d'entrée pour le login
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Instanciation de la façade métier
facade = HBnBFacade()


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'JWT token returned')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authentifie l'utilisateur et renvoie un jeton JWT"""
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])

        # Vérification des identifiants
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Encodage avec identité str + claims admin
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "is_admin": bool(user.is_admin)
            }
        )

        return {'access_token': access_token}, 200


@api.route('/protected')
class Protected(Resource):
    @jwt_required()
    @api.response(200, 'Access granted')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """Un point de terminaison protégé nécessitant un JWT valide"""
        identity = get_jwt_identity()
        claims = get_jwt()
        return {
            'message': f"Hello, user {identity}",
            'is_admin': claims.get('is_admin')
        }, 200
