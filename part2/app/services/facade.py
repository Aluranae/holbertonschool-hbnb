import uuid
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==========================
    # Gestion de User
    # ==========================

    # Récupération d'un utilisateur par ID
    def get_user(self, user_id):
        """
        Récupère un utilisateur par son identifiant (UUID ou string).
        Retourne l'objet User ou None si non trouvé ou mal formaté.
        """
        try:
            user_id = uuid.UUID(user_id)  # Convertit la chaîne en UUID si besoin
        except (ValueError, TypeError):
            return None
        return self.user_repo.get(user_id)

    def get_user_by_id(self, user_id):
        """
        Alias explicite de get_user pour répondre à certains besoins métier/
        API.
        """
        return self.get_user(user_id)

    def get_user_by_email(self, email):
        """
        Recherche un utilisateur par adresse e-mail.
        Retourne l'objet User correspondant ou None si non trouvé.
        """
        return next(
            (user for user in self.user_repo.get_all() if user.email == email),
            None
        )

    def get_all_users(self):
        """
        Retourne la liste de tous les utilisateurs.
        """
        return self.user_repo.get_all()

    def create_user(self, user_data):
        """
        Crée un nouvel utilisateur à partir d'un dictionnaire de données.
        Exige : first_name, last_name, email (is_admin est optionnel).
        Vérifie que l'e-mail n'est pas déjà utilisé.
        Lève une ValueError si doublon ou données invalides.
        """
        # Vérifie l'unicité de l'e-mail
        if self.get_user_by_email(user_data["email"]):
            raise ValueError("Email already registered")

        try:
            user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
                is_admin=user_data.get("is_admin", False)
            )
            self.user_repo.add(user)
            return user
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Invalid user data: {e}")

    def update_user(self, user_id, update_data):
        """
        Met à jour un utilisateur existant avec les données fournies.
        Lève une ValueError si l'utilisateur n'existe pas.
        """
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        user.update(update_data)  # méthode fournie par BaseModel
        self.user_repo.add(user)  # réécriture dans le stockage
        return user

    def delete_user(self, user_id):
        """
        Supprime un utilisateur par son identifiant.
        Retourne True si suppression réussie, False sinon.
        """
        if self.get_user(user_id):
            self.user_repo.delete(user_id)
            return True
        return False

    # ==========================
    # Gestion de Place
    # ==========================

    # Méthode placeholder pour récupérer un place par ID
    def create_place(self, place_data):
        """
        Crée un nouveau lieu à partir d'un dictionnaire de données.
        Exige : title, description, price, latitude, longitude, owner_id.
        Optionnel : amenities (liste d'objets Amenity ou d'ID)
        """
        try:
            owner = self.user_repo.get(place_data["owner_id"])
            if not owner:
                raise ValueError("Owner not found")

            amenities = place_data.get("amenities", [])

            place = Place(
                title=place_data["title"],
                description=place_data["description"],
                price=place_data["price"],
                latitude=place_data["latitude"],
                longitude=place_data["longitude"],
                owner=owner
            )

            # Ajout des commodités si elles sont valides
            for amenity in amenities:
                if isinstance(amenity, Amenity):
                    place.add_amenity(amenity)
                elif isinstance(amenity, str):  # ID de l’amenity
                    a = self.amenity_repo.get(amenity)
                    if a:
                        place.add_amenity(a)

            self.place_repo.add(place)
            return place

        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Invalid place data: {e}")

    def get_place(self, place_id):
        """
        Récupère un lieu par son identifiant.
        """
        return self.place_repo.get(place_id)

    def get_place_by_title(self, title):
        """
        Recherche un lieu par son titre exact (sensible à la casse).
        Retourne l'objet Place ou None si non trouvé.
        """
        return next(
            (place for place in self.place_repo.get_all() if place.title ==
             title),
            None
        )

    def get_all_places(self):
        """
        Retourne la liste de tous les lieux enregistrés.
        """
        return self.place_repo.get_all()

    def get_places_by_user(self, user_id):
        """
        Retourne la liste des lieux appartenant à un utilisateur donné.
        Utile pour afficher tous les logements d’un hôte.
        """
        return [
            place for place in self.place_repo.get_all()
            if place.owner and place.owner.id == user_id
        ]

    def update_place(self, place_id, update_data):
        """
        Met à jour un lieu existant avec les données fournies.
        Les commodités peuvent être mises à jour via la clé 'amenities'.
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found")

        # Séparation de la liste des amenities, si présente
        amenities = update_data.pop("amenities", None)

        # Mise à jour des autres champs (title, price, etc.)
        place.update(**update_data)

        # Mise à jour des amenities si fournie
        if amenities is not None:
            place.amenities.clear()
            for amenity in amenities:
                if isinstance(amenity, Amenity):
                    place.add_amenity(amenity)
                elif isinstance(amenity, str):
                    a = self.amenity_repo.get(amenity)
                    if a:
                        place.add_amenity(a)

        self.place_repo.add(place)
        return place

    def delete_place(self, place_id):
        """
        Supprime un lieu par son identifiant.
        Retourne True si suppression réussie, False sinon.
        """
        if self.get_place(place_id):
            self.place_repo.delete(place_id)
            return True
        return False

    # ==========================
    # Gestion de Amenity
    # ==========================

    # Gestion des commodités (Amenity)
    def create_amenity(self, amenity_data):
        """
        Crée une nouvelle commodité à partir d'un dictionnaire de données.
        Exige : name (obligatoire).
        """
        try:
            amenity = Amenity(name=amenity_data["name"])
            self.amenity_repo.add(amenity)
            return amenity
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Invalid amenity data: {e}")

    def get_amenity(self, amenity_id):
        """
        Récupère une commodité par son identifiant.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retourne la liste de toutes les commodités enregistrées.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, update_data):
        """
        Met à jour le nom d'une commodité existante.
        Exige une clé 'name' dans update_data.
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")

        if "name" not in update_data:
            raise ValueError("Missing 'name' in update data")

        amenity.name = update_data["name"]  # setter avec validation intégrée
        self.amenity_repo.add(amenity)
        return amenity

    def delete_amenity(self, amenity_id):
        """
        Supprime une commodité par son identifiant.
        Retourne True si suppression réussie, False sinon.
        """
        if self.get_amenity(amenity_id):
            self.amenity_repo.delete(amenity_id)
            return True
        return False

    # ==========================
    # Gestion de Review
    # ==========================

    # Création d'un nouvel avis utilisateur
    def create_review(self, review_data):
        """
        Crée un nouvel avis à partir d'un dictionnaire de données.
        Exige : text, rating, author_id, place_id.
        """
        try:
            author = self.user_repo.get(review_data["author_id"])
            if not author:
                raise ValueError("Author not found")

            place = self.place_repo.get(review_data["place_id"])
            if not place:
                raise ValueError("Place not found")

            review = Review(
                text=review_data["text"],
                rating=review_data["rating"],
                author=author,
                place=place
            )
            self.review_repo.add(review)
            place.add_review(review)  # synchronisation relationnelle
            self.place_repo.add(place)  # re-save du lieu avec la review liée
            return review

        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Invalid review data: {e}")

    def get_review(self, review_id):
        """
        Récupère un avis par son identifiant.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retourne la liste de tous les avis enregistrés.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retourne la liste des avis associés à un lieu donné.
        Retourne [] si aucun.
        """
        return [
            review for review in self.review_repo.get_all()
            if review.place and review.place.id == place_id
        ]

    def update_review(self, review_id, update_data):
        """
        Met à jour le texte et/ou la note d'un avis existant.
        Ne modifie ni l’auteur ni le lieu associé.
        """
        review = self.get_review(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")

        if "text" in update_data:
            review.text = review.validate_text(update_data["text"], "Text")

        if "rating" in update_data:
            review.rating = review.validate_rating(update_data["rating"],
                                                   "Rating")

        self.review_repo.add(review)
        return review

    def delete_review(self, review_id):
        """
        Supprime un avis par son identifiant.
        Met aussi à jour la liste des reviews dans l’objet Place lié.
        """
        review = self.get_review(review_id)
        if not review:
            return False

        # Nettoyage de la relation dans le Place concerné
        place = review.place
        if place and review in place.reviews:
            place.reviews.remove(review)
            self.place_repo.add(place)

        self.review_repo.delete(review_id)
        return True
