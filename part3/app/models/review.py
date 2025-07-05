"""models/review.py

Modèle SQLAlchemy enrichi représentant un avis utilisateur dans HBnB.
Hérite de BaseModel. Cette version mappe les relations avec User et Place.
"""

from app import db
from app.models.base import BaseModel


class Review(BaseModel):
    """
    Modèle représentant un avis utilisateur sur un lieu.

    Hérite de :
    - BaseModel : fournit id, created_at, updated_at

    Attributs :
    - text (str) : contenu de l'avis (obligatoire, max 500 caractères)
    - rating (int) : note sur 5 (obligatoire, entre 1 et 5)
    - user_id (str) : ID de l’auteur (clé étrangère)
    - place_id (str) : ID du lieu (clé étrangère)
    - author : relation vers User (déduite via backref="author")
    - place : relation vers Place (déduite via backref="place")
    """

    __tablename__ = "reviews"

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey("places.id"), nullable=False)

    # Les relations sont gérées via backref (dans User et Place), donc rien à définir ici

    # ========== VALIDATIONS ==========

    def validate_text(self, value, field_name):
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > 500:
            raise ValueError(f"{field_name} must be at most 500 characters")
        return value

    def validate_rating(self, value, field_name):
        if not isinstance(value, int):
            raise TypeError(f"{field_name} must be an integer")
        if not (1 <= value <= 5):
            raise ValueError(f"{field_name} must be between 1 and 5")
        return value

    def validate_author(self, value, field_name):
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError(f"{field_name} must be an instance of User")
        return value

    def validate_place(self, value, field_name):
        from app.models.place import Place
        if not isinstance(value, Place):
            raise TypeError(f"{field_name} must be an instance of Place")
        return value

    # ========== MÉTHODES MÉTIER ==========

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "text":
                self.text = self.validate_text(value, "Text")
            elif key == "rating":
                self.rating = self.validate_rating(value, "Rating")
            elif key == "author":
                self.user_id = self.validate_author(value, "Author").id
            elif key == "place":
                self.place_id = self.validate_place(value, "Place").id

    # ========== REPRÉSENTATIONS ==========

    def __repr__(self):
        return f"<Review {self.id}: {self.rating}⭐ by {self.user_id}>"

    def __str__(self):
        return (
            f"[Review] {self.author.first_name} {self.author.last_name} "
            f"sur {self.place.title} : {self.rating}⭐ - \"{self.text}\""
        )

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
