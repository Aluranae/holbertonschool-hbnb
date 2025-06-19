from flask_restx import Namespace, Resource

api = Namespace('amenities', description='Amenities related operations')

@api.route('/')
class AmenityList(Resource):
    def get(self):
        return {'amenities': []}  # Exemple basique
