from abc import ABC, abstractmethod
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    """
    Implémentation générique d’un repository basé sur SQLAlchemy.
    Gère les opérations CRUD standard pour n’importe quel modèle SQLAlchemy.
    """
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()


class UserRepository(SQLAlchemyRepository):
    """
    Repository spécifique pour les objets User.
    Permet des requêtes personnalisées sur les utilisateurs.
    """
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        """
        Récupère un utilisateur à partir de son email (unique).

        Paramètres :
        - email (str) : email de l'utilisateur

        Retour :
        - User ou None
        """
        return self.model.query.filter_by(email=email).first()


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)