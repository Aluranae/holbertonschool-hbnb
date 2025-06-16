"""models/review.py

Définit la classe Review, représentant un avis utilisateur
dans l'application HBnB.
Cette classe hérite de BaseModel et contient les attributs
spécifiques à un avis.
"""

# Import de la classe de base
from models.base import BaseModel

# Import des classes nécessaires pour les validations de type
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """
    Classe représentant un avis utilisateur sur un lieu.

    Hérite de :
    - BaseModel : fournit id, created_at, updated_at

    Attributs spécifiques :
    - text (str) : contenu de l'avis (obligatoire, max 500 caractères)
    - rating (int) : note sur 5 (obligatoire, entier entre 1 et 5)
    - author (User) : utilisateur ayant rédigé l'avis
    (doit être une instance de User)
    - place (Place) : lieu concerné par l'avis
    (doit être une instance de Place)
    """

    def __init__(self, text, rating, author, place):
        """
        Constructeur de la classe Review.

        Paramètres :
        - text (str) : contenu de l'avis
        - rating (int) : note entre 1 et 5
        - author (User) : utilisateur ayant rédigé l'avis
        - place (Place) : lieu concerné par l'avis
        """
        super().__init__()
        self.text = self.validate_text(text, "Text")
        self.rating = self.validate_rating(rating, "Rating")
        self.author = self.validate_author(author, "Author")
        self.place = self.validate_place(place, "Place")

    # ==========================
    # MÉTHODES DE VALIDATION
    # ==========================

    def validate_text(self, value, field_name):
        """Valide le contenu du texte : str non vide, max 500 caractères."""
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > 500:
            raise ValueError(f"{field_name} must be at most 500 characters")
        return value

    def validate_rating(self, value, field_name):
        """Valide la note : int entre 1 et 5."""
        if not isinstance(value, int):
            raise ValueError(f"{field_name} must be an integer")
        if not (1 <= value <= 5):
            raise ValueError(f"{field_name} must be between 1 and 5")
        return value

    def validate_author(self, value, field_name):
        """Valide l’auteur : doit être une instance de User."""
        if not isinstance(value, User):
            raise TypeError(f"{field_name} must be an instance of User")
        return value

    def validate_place(self, value, field_name):
        """Valide le lieu : doit être une instance de Place."""
        if not isinstance(value, Place):
            raise TypeError(f"{field_name} must be an instance of Place")
        return value

    # ==========================
    # MÉTHODE TECHNIQUE
    # ==========================

    def __repr__(self):
        """
        Représentation technique de l'avis, utile pour le debug.
        Exemple : <Review 78c1... - 5>
        """
        return (
            f"<Review {self.id}: rating={self.rating}, "
            f"author={self.author.id}>"
        )
