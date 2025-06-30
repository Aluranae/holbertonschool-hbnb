"""models/place.py

Définit la classe Place, représentant un logement dans l'application HBnB.
Cette classe hérite de BaseModel et contient les attributs
spécifiques liés à un lieu.
"""

# Imports nécessaires
# BaseModel : classe de base commune
from app.models.base import BaseModel
# Importer le modèle User pour vérifier le type du propriétaire
from app.models.user import User
# Importer le modèle User pour vérifier le type de amenity
from app.models.amenity import Amenity


class Place(BaseModel):
    """
    Classe représentant un lieu (hébergement) dans l'application HBnB.

    Hérite de :
    - BaseModel : fournit id, created_at, updated_at

    Attributs spécifiques :
    - title (str) : titre du lieu (obligatoire, max 100 caractères)
    - description (str) : description du lieu (optionnelle)
    - price (float) : prix par nuit (obligatoire, positif)
    - latitude (float) : latitude géographique (-90.0 à 90.0)
    - longitude (float) : longitude géographique (-180.0 à 180.0)
    - owner (User) : instance User représentant le propriétaire (doit exister)
    - reviews (list) : liste des avis associés (instances Review)
    - amenities (list) : liste des commodités associées (instances Amenity)
    """

    __slots__ = BaseModel.__slots__ + (
        'title',
        'description',
        'price',
        'latitude',
        'longitude',
        'owner',
        'reviews',
        'amenities'
    )

    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Constructeur de la classe Place.

        Paramètres :
        - title (str) : titre du lieu (obligatoire, <= 100 caractères)
        - description (str) : texte descriptif du lieu (optionnel)
        - price (float) : tarif par nuit (obligatoire, > 0)
        - latitude (float) : position géographique (entre -90.0 et 90.0)
        - longitude (float) : position géographique (entre -180.0 et 180.0)
        - owner (User) : propriétaire du lieu (doit être une instance de User)
        """
        super().__init__()
        self.title = self.validate_title(title, "Title")
        self.description = self.validate_description(description,
                                                     "Description")
        self.price = self.validate_price(price, "Price")
        self.latitude = self.validate_latitude(latitude, "Latitude")
        self.longitude = self.validate_longitude(longitude, "Longitude")
        self.owner = self.validate_owner(owner, "Owner")
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    # ==========================
    # MÉTHODES DE VALIDATION
    # ==========================

    def validate_title(self, value, field_name):
        """Valide un titre : type str, non vide, max 100 caractères."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > 100:
            raise ValueError(f"{field_name} must be at most 100 characters")
        return value

    def validate_description(self, value, field_name):
        """Valide une description : type str, non vide."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} is required")
        return value

    def validate_price(self, value, field_name):
        """Valide un prix : type float ou int, strictement positif."""
        if isinstance(value, bool) or not isinstance(value, (float, int)):
            raise TypeError(f"{field_name} must be an int or a float")
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")
        return value

    def validate_latitude(self, value, field_name):
        """Valide une latitude : float entre -90.0 et 90.0."""
        if not isinstance(value, float):
            raise TypeError(f"{field_name} must be a float")
        if not (-90.0 <= value <= 90.0):
            raise ValueError(f"{field_name} must be between -90.0 and/or 90.0")
        return value

    def validate_longitude(self, value, field_name):
        """Valide une longitude : float entre -180.0 et 180.0."""
        if not isinstance(value, float):
            raise TypeError(f"{field_name} must be a float")
        if not (-180.0 <= value <= 180.0):
            raise ValueError(f"{field_name} must be between -180.0 and 180.0")
        return value

    def validate_owner(self, value, field_name):
        """Valide le propriétaire : doit être une instance de User."""
        if not isinstance(value, User):
            raise TypeError(f"{field_name} must be an instance of User")
        return value

    def validate_review(self, value, field_name):
        """
        Valide un objet Review : doit être une instance de la classe Review."""
        # Importer le modèle User pour vérifier le type de review
        # Import local pour casser la boucle
        from app.models.review import Review
        if not isinstance(value, Review):
            raise TypeError(f"{field_name} must be an instance of Review")
        return value

    def validate_amenity(self, value, field_name):
        """
        Valide un objet Amenity : doit être une instance de la classe Amenity.
        """
        if not isinstance(value, Amenity):
            raise TypeError(f"{field_name} must be an instance of Amenity")
        return value

    # ============================
    # MÉTHODES METIER PRINCIPALES
    # ============================

    def add_review(self, review):
        """
        Ajoute un avis à la liste des reviews du lieu.

        Paramètre :
        - review (Review) : instance représentant un avis utilisateur
        """
        self.validate_review(review, "Review")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Ajoute une commodité à la liste des amenities du lieu.

        Paramètre :
        - amenity (Amenity) : instance représentant une commodité
        """
        self.validate_amenity(amenity, "Amenity")
        self.amenities.append(amenity)

    def update(self, **kwargs):
        """
        Met à jour les attributs de l'instance Place en validant chaque champ.
        """
        for key, value in kwargs.items():
            if key == "title":
                self.title = self.validate_title(value, "Title")
            elif key == "description":
                self.description = self.validate_description(value,
                                                             "Description")
            elif key == "price":
                self.price = self.validate_price(value, "Price")
            elif key == "latitude":
                self.latitude = self.validate_latitude(value, "Latitude")
            elif key == "longitude":
                self.longitude = self.validate_longitude(value, "Longitude")
            elif key == "owner":
                self.owner = self.validate_owner(value, "Owner")

        self.save()  # met à jour updated_at

    def __repr__(self):
        """
        Représentation technique du lieu, utile pour le debug.
        Exemple : <Place 78c1... - Cozy Apartment>
        """
        return f"<Place {self.id}: {self.title}>"

    def __str__(self):
        return (
            f"[Place] {self.title} ({self.id})\n"
            f"Description: {self.description}\n"
            f"Price: {self.price} credits/night\n"
            f"Location: ({self.latitude}, {self.longitude})\n"
            f"Owner: {self.owner.first_name} {self.owner.last_name}\n"
            f"({self.owner.email})"
        )
