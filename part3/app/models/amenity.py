"""models/amenity.py

Définit la classe Amenity, représentant une commodité disponible
dans un lieu de l'application HBnB.
Cette classe hérite de BaseModel.
"""

# Import de la classe de base
from app.models.base import BaseModel


class Amenity(BaseModel):
    """
    Classe représentant une commodité associée à un hébergement.

    Hérite de :
    - BaseModel : fournit id, created_at, updated_at

    Attributs spécifiques :
    - name (str) : nom de la commodité (obligatoire, max 50 caractères)
    """

    __slots__ = BaseModel.__slots__ + ('_name',)

    def __init__(self, name):
        """
        Constructeur de la classe Amenity.

        Paramètre :
        - name (str) : nom de la commodité (ex: "Wi-Fi", "Parking")
        """
        super().__init__()
        self._name = self.validate_name(name, "Name")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.validate_name(value, "Name")
        self.touch()  # méthode héritée de BaseModel pour mettre à jour updated_at

    # ==========================
    # MÉTHODE DE VALIDATION
    # ==========================

    def validate_name(self, value, field_name):
        """
        Valide le nom de la commodité : str non vide, max 50 caractères.
        """
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > 50:
            raise ValueError(f"{field_name} must be at most 50 characters")
        return value

    # ==========================
    # MÉTHODE TECHNIQUE
    # ==========================

    def __repr__(self):
        """
        Représentation technique de l'amenity, utile pour le debug.
        Exemple : <Amenity 78c1... - Wi-Fi>
        """
        return f"<Amenity {self.id}: {self.name}>"

    def __str__(self):
        """
        Affichage lisible d'une commodité.
        Exemple : Commodité : Wi-Fi
        """
        return f"Commodité : {self.name}"
