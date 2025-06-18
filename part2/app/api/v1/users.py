from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Modèle d'entrée (sans ID)
user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# Modèle de sortie (hérite du modèle d'entrée + id)
user_output_model = api.inherit('UserOutput', user_input_model, {
    'id': fields.String(readonly=True, description='User ID')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_input_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_output_model)
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Check email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, 'Email already registered')

        new_user = facade.create_user(user_data)
        return new_user, 201

    @api.marshal_list_with(user_output_model)
    def get(self):
        """List all users"""
        return facade.get_all_users(), 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.expect(user_input_model, validate=False)
    @api.marshal_with(user_output_model)
    def put(self, user_id):
        """Update a user"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        user_data = api.payload

        if "email" in user_data:
            existing_user = facade.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                api.abort(400, "Email already registered")

        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user, 200
        except ValueError as e:
            api.abort(400, str(e))
