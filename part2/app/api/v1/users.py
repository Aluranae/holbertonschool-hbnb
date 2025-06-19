from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_model, as_list=True)
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return [{
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email
        } for u in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.expect(user_model, validate=False)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Updates a user"""
        user = facade.get_user(user_id)
        if not user :
            api.abort(404, "User  ot found")

        try:
            updated_user = facade.update_user(user_id, api.payload)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name, 
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except ValueError as e:
            api.abort(400, str(e))