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
from flask_bcrypt import Bcrypt  # Import nécessaire pour les méthodes de hachage
bcrypt = Bcrypt()


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
                                       'password', 'is_admin', 'places',
                                       'reviews')

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
        - password (str) : mot de passe haché
        - is_admin (bool, optionnel) :
        booléen indiquant si l'utilisateur est admin (défaut : False)
        """
        super().__init__()
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.password = None  # ← Mot de passe haché, initialisé à None
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

    def hash_password(self, password):
        """
        Hash le mot de passe avec bcrypt après avoir appliqué
        une politique de sécurité stricte.

        Paramètres :
        - password (str) : mot de passe en clair fourni par l'utilisateur.

        Règles de sécurité :
        - Au moins 12 caractères
        - Au moins une lettre minuscule
        - Au moins une lettre majuscule
        - Au moins un chiffre
        - Au moins un caractère spécial (non alphanumérique)

        Comportement :
        - Si le mot de passe ne respecte pas les règles, une ValueError est levée.
        - Si le mot de passe est invalide (ex : None ou mauvais type), une TypeError est levée.
        - Sinon, le mot de passe est haché et stocké dans self.password.
        """

        # Vérification de type
        # Lever TypeError sinon
        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        # Nettoyage : supprimer les espaces en début/fin (si pertinent)
        password = password.strip()
        if not password:
            raise ValueError("Password is required")

        # Vérification des règles de sécurité :

        # Règle 1 : longueur minimale
        if len(password) < 12:
            raise ValueError("Password must be at least 12 characters")

        # Règle 2 : au moins une lettre minuscule
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")

        # Règle 3 : au moins une lettre majuscule
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")

        # Règle 4 : au moins un chiffre
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number")

        # Règle 5 : au moins un caractère spécial
        if not re.search(r"[^\w\s]", password):
            raise ValueError("Password must contain at least one special character")

        # Hachage avec bcrypt
        # Génère le hash avec bcrypt
        # Décodez le résultat (UTF-8) et stockez dans self.password
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

        self.save()

    def verify_password(self, password):
        """
            Vérifie si le mot de passe en clair correspond au hash stocké.

        Paramètres :
        - password (str) : mot de passe en clair fourni pour vérification.

        Retour :
        - bool : True si le mot de passe correspond au hash,
                False sinon.

        Comportement :
        - Utilise bcrypt.check_password_hash() pour comparer.

        Exceptions :
        - ValueError si aucun mot de passe n’est stocké.
        - TypeError si l'entrée n’est pas une chaîne de caractères.
        """
        # Vérifier que self.password n’est pas None
        if not self.password:
            raise ValueError("Password is not set")
        # Vérifier que password est une chaîne
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        # Utiliser bcrypt.check_password_hash() pour comparer
        return bcrypt.check_password_hash(self.password, password)

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