"""models/base.py

Définit la classe de base pour toutes les entités métier de l'application HBnB.
Cette classe centralise les attributs communs et fournit des méthodes
utilitaires telles que la sauvegarde (mise à jour de `updated_at`)
et la mise à jour d'attributs à partir d'un dictionnaire.

Toutes les entités (User, Place, Review, Amenity) hériteront de cette classe.
"""

# Imports nécessaires
# uuid : pour générer un identifiant unique (UUID v4) sous forme de chaîne
# datetime : pour générer les horodatages de création et mise à jour
import uuid
from datetime import datetime, timezone


class BaseModel:
    """
    Classe de base commune aux entités métier de l'application.

    Attributs publics :
    - id (str) : identifiant unique de l'instance
    (UUID v4 sous forme de chaîne)
    - created_at (datetime) : date/heure de création de l'objet
    - updated_at (datetime) : date/heure de dernière modification de l'objet

    Méthodes :
    - save() : met à jour l'attribut `updated_at`
    - update(data: dict) : met à jour les attributs depuis un dictionnaire
    """

    __slots__ = ('_id', '_created_at', 'updated_at')  # limitation explicite des attributs

    def __init__(self):
        """
        Constructeur commun à toutes les entités métier.
        """
        now = datetime.now(timezone.utc)
        self._id = str(uuid.uuid4())
        self._created_at = now
        self.updated_at = now

    def touch(self):
        """Met à jour updated_at à l'heure actuelle en UTC (aware)."""
        self.updated_at = datetime.now(timezone.utc)

    @property
    def id(self):
        """Accès en lecture à l'identifiant unique (lecture seule)."""
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("id is immutable")

    @property
    def created_at(self):
        """Accès en lecture à la date de création (lecture seule)."""
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        raise AttributeError("created_at is immutable")

    def __eq__(self, other):
        """
        Deux objets sont égaux s'ils ont le même identifiant.
        """
        return isinstance(other, self.__class__) and self.id == other.id

    def save(self):
        """
        Met à jour la date de dernière modification de l'objet.
        """
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data):
        """
        Met à jour dynamiquement les attributs de l'objet
        à partir d'un dictionnaire.

        Paramètre :
        - data (dict) : dictionnaire contenant des paires clé/valeur
                        où chaque clé correspond à un attribut de l'objet
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # met à jour `updated_at`

    def to_dict(self):
        result = {}
        for slot in self.__slots__:
            value = getattr(self, slot)
            if isinstance(value, datetime):
                result[slot] = value.isoformat()
            else:
                result[slot] = value
        result['__class__'] = self.__class__.__name__
        return result
