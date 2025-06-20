from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_restx import marshal

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)', min=1, max=5),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_output_model = api.inherit('ReviewOut', review_model, {
    'id': fields.String(readonly=True, description='Review ID')
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
    @api.response(500, 'Internal server error')
    def put(self, review_id):
        """
        Update a review's information by its ID.
        """
        try:
            updated_review = facade.update_review(review_id, api.payload)

            if not updated_review:
                return {"error": "Review not found"}, 404

            # Retourne l'objet mis à jour sous forme de dict propre
            return updated_review.to_dict(), 200

        except ValueError as e:
            # Cas explicite : champ manquant, mauvais ID, etc.
            msg = str(e)
            if "not found" in msg.lower():
                return {"error": msg}, 404
            return {"error": msg}, 400

        except Exception as e:
            # Cas inattendu (ex: problème interne)
            print(f"[ERROR] PUT /reviews/{review_id}: {e}")
            return {"error": "Internal server error"}, 500

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
    @api.response(404, 'Place not found or no reviews available')
    @api.response(500, 'Internal server error')
    def get(self, place_id):
        """
        Get all reviews for a specific place.
        """
        try:
            reviews = facade.get_reviews_by_place(place_id)

            if not reviews:
                return {"error": "No reviews found for this place"}, 404

            return marshal(reviews, review_output_model), 200

        except ValueError as e:
            if "Place not found" in str(e):
                return {"error": str(e)}, 404
            return {"error": str(e)}, 400

        except Exception as e:
            print(f"[ERROR] Unexpected error in PlaceReviewList: {e}")
            return {"error": "Internal server error"}, 500


@api.route('/users/<string:user_id>/reviews')
class UserReviewList(Resource):
    @api.response(200, 'List of reviews for the user retrieved successfully')
    @api.response(404, 'User not found or no reviews found')
    @api.response(500, 'Internal server error')
    def get(self, user_id):
        """
        Get all reviews written by a specific user.
        """
        try:
            # Récupère les reviews depuis la couche métier
            reviews = facade.get_reviews_by_user(user_id)

            # Si l'utilisateur existe mais n'a posté aucun avis
            if not reviews:
                return {"error": "No reviews found for this user"}, 404

            # Appliquer manuellement le modèle uniquement ici
            return marshal(reviews, review_output_model), 200

        except ValueError as e:
            # Cas explicite : utilisateur introuvable
            if "User not found" in str(e):
                return {"error": str(e)}, 404
            return {"error": str(e)}, 400

        except Exception as e:
            # En cas d'erreur imprévue (debug possible ici)
            print(f"[ERROR] Unexpected error in UserReviewList: {e}")
            return {"error": "Internal server error"}, 500
