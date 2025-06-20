"""
api/v1/places.py

Définit les endpoints pour la gestion des lieux (Place) dans l'application
HBnB.
Utilise Flask-RESTx pour définir l'API RESTful.

Chaque endpoint interagit avec la couche de logique métier via la facade
HBnBFacade.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade  # Accès à la couche métier

# ===================================================
# Définition du Namespace pour les opérations Place
# ===================================================
api = Namespace('places', description='Place operations')

# ===================================================
# Définition du modèle Amenity (utilisé en réponse)
# ===================================================
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# ===================================================
# Définition du modèle User (utilisé en réponse)
# ===================================================
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# ===================================================
# Définition du modèle Place (reçu en entrée POST/PUT)
# ===================================================
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


# ===================================================
# /api/v1/places/
# Ressource pour créer ou lister tous les lieux
# ===================================================
@api.route('/')
class PlaceList(Resource):

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner Not Found')
    @api.response(409, 'Conflict: Title already used by this owner')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """
        Enregistre un nouveau lieu (place) à partir des données JSON reçues.
        """
        # Récupération et vérification du JSON reçu
        data = request.get_json()
        if not data:
            return {"error": "Missing or invalid JSON data"}, 400

        try:
            # Extraction de title et owner_id
            title = data.get("title")
            owner_id = data.get("owner_id")

            # Vérification de l'existence du propriétaire
            owner = facade.get_user(owner_id)
            if not owner:
                return {"error": "Owner not found"}, 404

            # Vérification de l’unicité du titre pour ce owner
            existing_place = facade.get_place_by_title(title)
            if existing_place and existing_place.owner.id == owner_id:
                return {"error": "This owner already has a place with the same" 
                        "title"}, 409

            # Création du lieu
            new_place = facade.create_place(data)

            # Construction de la réponse JSON (à coder)
            response = {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id
            }

            return response, 201
        # Gestion des erreurs de validation ou données incorrectes
        # (champ manquant, mauvais type, etc.)
        except (ValueError, TypeError, KeyError) as e:
            return {"error": str(e)}, 400
        # Gestion des erreurs inattendues (ex : crash interne, bug imprévu)
        except Exception:
            return {"error": "Internal server error"}, 500  # Optionnel

    @api.response(200, 'List of places retrieved successfully')
    @api.response(500, 'Internal server error')
    def get(self):
        """
        Récupère la liste de tous les lieux enregistrés.
        """
        try:
            # - Appeler facade.get_all_places()
            places = facade.get_all_places()
            if not places:
                return {
                    "message": "No places found",
                    "places": []
                }, 200

            # - Transformer chaque Place en dictionnaire JSON, avec toutes les infos utiles
            result = []
            for place in places:
                result.append({
                    "id": place.id,
                    "title": place.title,
                    "description": place.description,
                    "price": place.price,
                    "latitude": place.latitude,
                    "longitude": place.longitude,
                    "owner_id": place.owner.id,
                    # - Ajouter la liste des amenities (id + name)
                    "amenities": [
                        {
                            "id": amenity.id,
                            "name": amenity.name
                        }
                        for amenity in place.amenities
                    ]
                })

            # - Retourner le message + liste formatée
            return {
                "message": "Places retrieved successfully",
                "places": result
            }, 200

        except Exception:
            # - En cas d'erreur serveur interne
            return {"error": "Internal server error"}, 500


# ===================================================
# /api/v1/places/<place_id>
# Ressource pour accéder ou modifier un lieu spécifique
# ===================================================
@api.route('/<place_id>')
class PlaceResource(Resource):

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @api.response(500, 'Internal server error')
    def get(self, place_id):
        """
        Récupère les détails d’un lieu spécifique par son ID.
        """
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner": {
                    "id": place.owner.id,
                    "first_name": place.owner.first_name,
                    "last_name": place.owner.last_name,
                    "email": place.owner.email
                },
                "amenities": [
                    {
                        "id": amenity.id,
                        "name": amenity.name
                    } for amenity in place.amenities
                ]
            }, 200

        except Exception:
            return {"error": "Internal server error"}, 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @api.response(409, 'Conflict: Title already used by this owner')
    @api.response(500, 'Internal server error')
    def put(self, place_id):
        """
        Met à jour les informations d’un lieu par son ID.
        """
        # - Vérification de l'existence du lieu
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # - Récupération et validation du JSON
        data = request.get_json()
        if not data:
            return {"error": "Missing or invalid JSON data"}, 400

        # - Préparation au traitement des amenities
        amenities_changed = False  # Flag de changement
        if "amenities" in data:
            amenities_ids = data.get("amenities")

            if not isinstance(amenities_ids, list):
                return {"error": "Field 'amenities' must be a list of IDs"}, 400

            amenities = []
            for amenity_id in amenities_ids:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {"error": f"Amenity with id '{amenity_id}' not found"}, 400
                amenities.append(amenity)

            # - Comparaison entre les anciennes et nouvelles amenities
            existing_ids = set(a.id for a in place.amenities)
            incoming_ids = set(amenities_ids)

            if existing_ids != incoming_ids:
                amenities_changed = True
                place.amenities = amenities  # Mise à jour en mémoire (hors repo)

        # - Comparaison combinée (champs simples + amenities)
        base_fields_unchanged = all(
            getattr(place, field) == data.get(field)
            for field in ['title', 'description', 'price', 'latitude', 'longitude']
            if data.get(field) is not None
        )

        if base_fields_unchanged and not amenities_changed:
            return {'error': 'No changes detected'}, 400

        # - Mise à jour finale via la facade
        try:
            facade.update_place(place_id, data)
            updated_place = facade.get_place(place_id)  # Rafraîchir les données

            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner.id,
                'amenities': [
                    {'id': amenity.id, 'name': amenity.name}
                    for amenity in updated_place.amenities
                ]
            }, 200

        except (ValueError, TypeError) as e:
            error_msg = str(e)
            if "Title already used" in error_msg:
                return {'error': error_msg}, 409
            return {'error': error_msg}, 400
