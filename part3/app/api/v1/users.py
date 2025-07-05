from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

api = Namespace('users', description='User operations')

# Modèle d'entrée (sans ID)
user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user', min_length=12)
})

# Modèle de sortie (hérite du modèle d'entrée + id)
user_output_model = api.model('UserOutput', {
    'id': fields.String(readonly=True, description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Whether the user is an admin')
})


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_input_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_output_model)
    def post(self):
        """Create a new user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        # Vérifie l'unicité de l'email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, 'Email already registered')

        try:
            new_user = facade.create_user(user_data)
            return new_user, 201
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

    @api.marshal_list_with(user_output_model)
    def get(self):
        """List all users"""
        return facade.get_all_users(), 200


@api.route('/search')
class UserSearch(Resource):
    @api.doc(params={'email': 'Email address of the user'})
    @api.marshal_with(user_output_model)
    @api.response(200, 'User found')
    @api.response(400, 'Missing email query parameter')
    @api.response(404, 'User not found')
    def get(self):
        """Search a user by email"""
        email = request.args.get('email')
        if not email:
            return {'error': "Missing 'email' query parameter"}, 400

        user = facade.get_user_by_email(email)
        if not user:
            return {'error': "User not found"}, 404

        return user, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.marshal_with(user_output_model)
    @api.response(200, 'User retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        return user, 200

    @jwt_required()
    @api.expect(user_input_model, validate=False)
    @api.marshal_with(user_output_model)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update a user (admin or self)"""
        identity = get_jwt_identity()  # str(user.id)
        claims = get_jwt()
        current_user_id = identity
        is_admin = claims.get("is_admin", False)

        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        if not is_admin and user.id != current_user_id:
            api.abort(403, "Unauthorized action")

        user_data = api.payload

        # Gestion de la modification de l'email
        if 'email' in user_data:
            if not is_admin:
                return {'error': 'You cannot modify email'}, 400

            existing = facade.get_user_by_email(user_data['email'])
            if existing and existing.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Gestion de la modification du mot de passe
        if 'password' in user_data and not is_admin:
            return {'error': 'You cannot modify password'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user, 200
        except ValueError as e:
            api.abort(400, str(e))
