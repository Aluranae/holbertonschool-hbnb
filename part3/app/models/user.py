"""models/user.py

Définit la classe User, représentant un utilisateur dans l'application HBnB.
Cette classe hérite de BaseModel et ajoute les attributs spécifiques
liés à l'identité de l'utilisateur.
"""

# Imports nécessaires
import re
from app.extensions import db
from app.models.base import BaseModel
from flask_bcrypt import Bcrypt  # Import nécessaire pour les méthodes de hachage
bcrypt = Bcrypt()


class User(BaseModel):
    """
    Classe représentant un utilisateur de la plateforme HBnB.

    Hérite de :
    - BaseModel : fournit id, created_at, updated_at

    Attributs spécifiques :
    - first_name (str) : prénom de l'utilisateur (obligatoire, max 50 caractères)
    - last_name (str) : nom de l'utilisateur (obligatoire, max 50 caractères)
    - email (str) : adresse e-mail (obligatoire, unique, format email standard)
    - is_admin (bool) : droits administrateur (par défaut False)
    """

    __tablename__ = "users"

    # Déclaration des colonnes SQLAlchemy
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relations ORM
    places = db.relationship(
        "Place", backref="owner", lazy=True, cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review", backref="author", lazy=True, cascade="all, delete-orphan"
    )

    def validate_name(self, value, field_name):
        """Valide un nom (prénom ou nom) : type str, non vide, max 50 caractères."""
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
        Met à jour les champs autorisés de l'utilisateur à partir d'un dictionnaire,
        en appliquant les règles de validation métier si nécessaire.
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

    def hash_password(self, password):
        """
        Hash le mot de passe avec bcrypt après avoir appliqué
        une politique de sécurité stricte.
        """
        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        password = password.strip()
        if not password:
            raise ValueError("Password is required")

        if len(password) < 12:
            raise ValueError("Password must be at least 12 characters")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[^\w\s]", password):
            raise ValueError("Password must contain at least one special character")

        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.save()

    def verify_password(self, password):
        """
        Vérifie si le mot de passe en clair correspond au hash stocké.
        """
        if not self.password:
            raise ValueError("Password is not set")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        """Représentation technique de l'utilisateur (debug)."""
        return (
            f"<User {self.id}: {self.first_name} {self.last_name} "
            f"({self.email})>"
        )

    def __str__(self):
        """Représentation lisible : "Nom Prénom (email)"."""
        return f"{self.first_name} {self.last_name} ({self.email})"
