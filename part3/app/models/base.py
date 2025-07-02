"""
models/base.py

Définit la classe de base pour toutes les entités persistées de l'application HBnB.
Cette classe est commune à toutes les entités métiers (User, Place, Review, Amenity).
Elle est conçue pour être compatible avec SQLAlchemy et ne génère pas de table directe.

Rôles :
- Fournir un identifiant UUID
- Gérer les timestamps created_at / updated_at
- Fournir des méthodes utilitaires : save(), update(), to_dict()
"""

# 🔧 Imports nécessaires
# uuid : pour générer un identifiant unique
# datetime : pour stocker des horodatages
# db : instance SQLAlchemy (importée depuis app/extensions)
import uuid
from datetime import datetime
from app.extensions import db


class BaseModel(db.Model):
    """
    Modèle de base abstrait (non instanciable) pour toutes les entités.

    Toutes les classes ORM héritant de BaseModel auront automatiquement :
    - un identifiant UUID en tant que clé primaire
    - une date de création (created_at)
    - une date de dernière mise à jour (updated_at)
    """

    # Indique à SQLAlchemy de ne pas créer de table pour ce modèle
    __abstract__ = True

    # colonne id
    id = db.Column(db.String(36),
                   primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    # created_at
    created_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(datetime.timezone.utc))
    # updated_at
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(datetime.timezone.utc),
                           onupdate=lambda: datetime.now(datetime.timezone.utc))

    def save(self):
        """
        Met à jour manuellement la date de dernière modification (updated_at).
        Cette méthode peut être utilisée avant de déclencher un commit.
        """
        self.updated_at = datetime.now(datetime.timezone.utc)

    def update(self, data):
        """
        Met à jour dynamiquement les attributs de l'objet
        à partir d’un dictionnaire {clé: valeur}.

        Seules les clés correspondant à des attributs déjà
        existantsseront mises à jour.
        À la fin, l’attribut updated_at est mis à jour via self.save().
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def __eq__(self, other):
        """
        Deux objets sont considérés comme égaux s’ils :
        - appartiennent à la même classe,
        - ont le même identifiant (self.id == other.id)
        """
        return isinstance(other, self.__class__) and self.id == other.id

    def to_dict(self):
        """
        Convertit l’objet en dictionnaire JSON-serializable.

        - Les valeurs datetime sont converties en chaîne ISO 8601.
        - L’attribut __class__ est ajouté pour l’identification.
        - Les attributs internes (ex: SQLAlchemy) sont ignorés.
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "__class__": self.__class__.__name__
        }

    def __repr__(self):
        """
        Affichage lisible en console ou log.
        """
        return f"<{self.__class__.__name__} id={self.id}>"
