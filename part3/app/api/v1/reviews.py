from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
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
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_output_model)
    def post(self):
        """Register a new review"""
        data = api.payload
        current_user_id = get_jwt_identity()
        data['user_id'] = current_user_id

        place = facade.get_place(data['place_id'])
        if not place:
            api.abort(400, 'Invalid place_id')
        if place.owner.id == current_user_id:
            api.abort(403, 'You cannot review your own place')

        existing_reviews = facade.get_reviews_by_user(current_user_id)
        if any(r.place_id == data['place_id'] for r in existing_reviews):
            api.abort(409, 'You have already reviewed this place')

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

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_output_model)
    def put(self, review_id):
        """Update a review's information"""

        # Récupération de l'identité de l'utilisateur via le JWT
        user_id = get_jwt_identity()

        # Récupération de l'objet User correspondant
        user = facade.get_user(user_id)
        if not user:
            api.abort(401, "Unauthorized")

        # Récupération de la review ciblée
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        # Vérifie que seul l'auteur ou un admin peut modifier la review
        if not user.is_admin and review.user_id != user_id:
            api.abort(403, 'You can only edit your own reviews')

        # Mise à jour de la review
        try:
            data = api.payload
            data['user_id'] = user_id  # Injection explicite
            updated = facade.update_review(review_id, data)
            return updated
        except ValueError as e:
            msg = str(e)
            if msg.endswith('not found'):
                api.abort(404, msg)
            api.abort(400, msg)

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized')
    def delete(self, review_id):
        """Delete a review"""
        user_id = get_jwt_identity()
        user = facade.get_user(user_id)
        if not user:
            api.abort(401, "Unauthorized")

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        if not user.is_admin and review.user_id != user_id:
            api.abort(403, 'You can only delete your own reviews')

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            msg = str(e)
            if msg.endswith("not found"):
                api.abort(404, msg)
            api.abort(400, msg)


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
