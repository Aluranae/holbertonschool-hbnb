from abc import ABC, abstractmethod
from app.extensions import db
from app.models.user import User


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


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)


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
