"""models/place.py

Modèle SQLAlchemy enrichi représentant un lieu (hébergement) dans HBnB.
Hérite de BaseModel qui fournit id, created_at, updated_at.
"""

from app import db
from app.models.base import BaseModel
# Import requis pour les ForeignKey vers User et la table d'association Place-Amenity
from app.models.place_amenity import place_amenity


class Place(BaseModel):
    """
    Modèle SQLAlchemy représentant un hébergement dans l'application HBnB.

    Attributs :
    - title (str) : titre du lieu (obligatoire, max 100 caractères)
    - description (str) : description du lieu (obligatoire)
    - price (float) : prix par nuit (obligatoire)
    - latitude (float) : latitude géographique (facultatif)
    - longitude (float) : longitude géographique (facultatif)
    """

    __tablename__ = "places"

    # Colonnes de base
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # 🔗 Clé étrangère vers User (relation User → Place)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    # 🔗 Relation Place → Review (un-à-plusieurs)
    reviews = db.relationship(
        "Review", backref="place", lazy=True, cascade="all, delete-orphan"
    )

    # 🔗 Relation Place ↔ Amenity (plusieurs-à-plusieurs)
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        backref=db.backref("places", lazy=True),
        lazy="subquery"
    )

    def __init__(self, title, description, price, latitude=None, longitude=None):
        super().__init__()
        self.title = self.validate_title(title, "Title")
        self.description = self.validate_description(description, "Description")
        self.price = self.validate_price(price, "Price")
        self.latitude = self.validate_latitude(latitude, "Latitude")
        self.longitude = self.validate_longitude(longitude, "Longitude")

    # ========== MÉTHODES DE VALIDATION ==========

    def validate_title(self, value, field_name):
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > 100:
            raise ValueError(f"{field_name} must be at most 100 characters")
        return value

    def validate_description(self, value, field_name):
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} is required")
        return value

    def validate_price(self, value, field_name):
        if isinstance(value, bool) or not isinstance(value, (float, int)):
            raise TypeError(f"{field_name} must be a float or int")
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")
        return float(value)

    def validate_latitude(self, value, field_name):
        if value is None:
            return None
        if not isinstance(value, float):
            raise TypeError(f"{field_name} must be a float")
        if not (-90.0 <= value <= 90.0):
            raise ValueError(f"{field_name} must be between -90.0 and 90.0")
        return value

    def validate_longitude(self, value, field_name):
        if value is None:
            return None
        if not isinstance(value, float):
            raise TypeError(f"{field_name} must be a float")
        if not (-180.0 <= value <= 180.0):
            raise ValueError(f"{field_name} must be between -180.0 and 180.0")
        return value

    # ========== MÉTHODES MÉTIER ==========

    def update(self, **kwargs):
        """Met à jour les champs du modèle avec validation"""
        for key, value in kwargs.items():
            if key == "title":
                self.title = self.validate_title(value, "Title")
            elif key == "description":
                self.description = self.validate_description(value, "Description")
            elif key == "price":
                self.price = self.validate_price(value, "Price")
            elif key == "latitude":
                self.latitude = self.validate_latitude(value, "Latitude")
            elif key == "longitude":
                self.longitude = self.validate_longitude(value, "Longitude")

    def __repr__(self):
        return f"<Place {self.id}: {self.title}>"

    def __str__(self):
        return (
            f"[Place] {self.title} (ID: {self.id})\n"
            f"Description: {self.description}\n"
            f"Price: {self.price} credits/night\n"
            f"Location: ({self.latitude}, {self.longitude})"
        )
