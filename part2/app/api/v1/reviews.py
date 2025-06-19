from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)', min=1, max=5),
    'user_id': fields.String(required=True, description='ID of the author (User)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_output_model = api.model('ReviewOut', {
    'id': fields.String(readonly=True, description='Review ID'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)', min=1, max=5),
    'user_id': fields.String(attribute='user_id', description='ID of the author (User)'),
    'place_id': fields.String(attribute='place_id', description='ID of the place')
})

message_model = api.model('Message', {
    'message': fields.String(description='A response message')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_output_model)
    def post(self):
        """Register a new review"""
        data = api.payload
        try:
            review = facade.create_review(data)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_output_model)
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.marshal_with(review_output_model)
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_output_model)
    def put(self, review_id):
        """Update a review's information"""
        try:
            updated = facade.update_review(review_id, api.payload)
            return updated
        except ValueError as e:
            msg = str(e)
            if msg.endswith('not found'):
                api.abort(404, msg)
            api.abort(400, msg)

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError:
            api.abort(404, 'Review not found')

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_list_with(review_output_model)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return reviews, 200
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/users/<string:user_id>/reviews')
class UserReviewList(Resource):
    @api.response(200, 'List of reviews for the user retrieved successfully')
    @api.response(404, 'User not found or no reviews found')
    @api.marshal_list_with(review_output_model)
    def get(self, user_id):
        """Get all reviews written by a specific user"""
        try:
            reviews = facade.get_reviews_by_user(user_id)
            if not reviews:
                api.abort(404, "No reviews found for this user")
            return reviews, 200
        except Exception:
            api.abort(500, "Internal server error")
