"""models/user.py

Définit la classe User, représentant un utilisateur dans l'application HBnB.
Cette classe hérite de BaseModel et ajoute les attributs spécifiques
liés à l'identité de l'utilisateur.
"""

# Imports nécessaires
# BaseModel : classe de base commune
# re : regex pour la vérification du mail
import re
from app.models.base import BaseModel


class User(BaseModel):
    """
    Classe représentant un utilisateur de la plateforme HBnB.

    Hérite de :
    - BaseModel : fournit id, created_at, updated_at

    Attributs spécifiques :
    - first_name (str) : prénom de l'utilisateur
    (obligatoire, max 50 caractères)
    - last_name (str) : nom de l'utilisateur (obligatoire, max 50 caractères)
    - email (str) : adresse e-mail (obligatoire, unique, format email standard)
    - is_admin (bool) : droits administrateur (par défaut False)
    """

    __slots__ = BaseModel.__slots__ + ('first_name', 'last_name', 'email',
                                       'is_admin', 'places', 'reviews')

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Constructeur de la classe User.

        Paramètres :
        - first_name (str) :
        prénom de l'utilisateur (obligatoire, <= 50 caractères)
        - last_name (str) :
        nom de l'utilisateur (obligatoire, <= 50 caractères)
        - email (str) :
        adresse e-mail (obligatoire, format email standard attendu)
        - is_admin (bool, optionnel) :
        booléen indiquant si l'utilisateur est admin (défaut : False)
        """
        super().__init__()
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = bool(is_admin)
        self.places = []  # ← Relation un-à-plusieurs : User → [Place]
        self.reviews = []  # ← Relation un-à-plusieurs : User → [Review]

    def validate_name(self, value, field_name):
        """Valide un nom (prénom ou nom) : type str, non vide,
        max 50 caractères."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > 50:
            raise ValueError(f"{field_name} must be at most 50 characters")
        return value

    def validate_email(self, value):
        """Valide une adresse email : type str, non vide, format standard."""
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        value = value.strip().lower()
        if not value:
            raise ValueError("Email is required")
        if value.count("@") != 1:
            raise ValueError("Email must contain exactly one '@'")
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
            raise ValueError("Invalid email format")
        return value

    def update(self, data):
        """
        Redéfinit la méthode update spécifiquement pour User.
        Applique les règles de validation métier (notamment sur l'email).
        """
        for key, value in data.items():
            if key == "email":
                self.email = self.validate_email(value)
            elif key == "first_name":
                self.first_name = self.validate_name(value, "First name")
            elif key == "last_name":
                self.last_name = self.validate_name(value, "Last name")
            elif key == "is_admin":
                self.is_admin = bool(value)
            elif hasattr(self, key):
                setattr(self, key, value)

        self.save()

    def __repr__(self):
        """
        Représentation technique de l'utilisateur, utile pour le debug.
        Exemple : <User 78c1... - john.doe@example.com>
        """
        return (
            f"<User {self.id}: {self.first_name} {self.last_name} "
            f"({self.email})>"
        )

    def __str__(self):
        """
        Retourne une représentation lisible : "Nom Complet (email)"
        """
        return f"{self.first_name} {self.last_name} ({self.email})"
