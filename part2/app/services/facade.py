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
        Récupère un utilisateur par son identifiant.
        Retourne l'objet User ou None si non trouvé.
        """
        return self.user_repo.get(user_id)

    def get_user_by_id(self, user_id):
        """
        Alias explicite de get_user pour répondre à certains besoins métier/API.
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

    """ A activer plus tard
    def delete_user(self, user_id):

        Supprime un utilisateur par son identifiant.
        Retourne True si suppression réussie, False sinon.

        if self.get_user(user_id):
            self.user_repo.delete(user_id)
            return True
        return False
    """

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

    def get_places_by_owner(self, owner_id):
        """
        Retourne tous les lieux appartenant à un propriétaire donné.
        """
        return [
            p for p in self.place_repo.get_all()
            if hasattr(p, "owner") and p.owner and p.owner.id == owner_id
        ]

    def update_place(self, place_id, update_data):
        """
        Met à jour un lieu existant avec les données fournies.
        Les commodités peuvent être mises à jour via la clé 'amenities'.
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found")

        # - Vérification de conflit sur le titre
        if "title" in update_data and update_data["title"] != place.title:
            for other_place in self.get_places_by_owner(place.owner.id):
                if other_place.id != place.id and other_place.title == update_data["title"]:
                    raise ValueError("Title already used by this owner")

        # - Séparation de la liste des amenities, si présente
        amenities = update_data.pop("amenities", None)

        # - Mise à jour des autres champs
        place.update(**update_data)

        # - Mise à jour des amenities si fournie
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

    """ A activer plus tard
    def delete_place(self, place_id):
    
        Supprime un lieu par son identifiant.
        Retourne True si suppression réussie, False sinon.

        if self.get_place(place_id):
            self.place_repo.delete(place_id)
            return True
        return False
    """

    # ==========================
    # Gestion de Amenity
    # ==========================

    # Gestion des commodités (Amenity)
    def create_amenity(self, amenity_data):
        """
        Crée une nouvelle commodité.
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

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
        Met à jour une commodité existante.

        Soulève une erreur si l'amenity n'existe pas.
        """
        # - Récupération de l'amenity ciblée
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            # - Déclenchement d'une erreur claire si l'ID est inconnu
            raise ValueError(f"Amenity with ID {amenity_id} not found")

        # - Mise à jour des champs
        for key, value in update_data.items():
            setattr(amenity, key, value)

        # - Mise à jour dans le repo
        self.amenity_repo.update(amenity_id, update_data)

        return amenity

    # ==========================
    # Gestion de Review
    # ==========================

    # Création d'un nouvel avis utilisateur
    def create_review(self, review_data):
        """
        Crée un nouvel avis à partir d'un dictionnaire de données.
        Exige : text, rating, user_id, place_id.
        """
        try:
            # correspondance avec le champ attendu par Swagger
            user = self.user_repo.get(review_data["user_id"])
            if not user:
                raise ValueError("User not found")

            place = self.place_repo.get(review_data["place_id"])
            if not place:
                raise ValueError("Place not found")

            review = Review(
                text=review_data["text"],
                rating=review_data["rating"],
                author=user,  # l’attribut dans Review reste "author"
                place=place
            )

            self.review_repo.add(review)
            place.add_review(review)      # synchronisation relationnelle
            self.place_repo.add(place)    # re-save du lieu avec la review liée

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
        Soulève une erreur si le lieu est introuvable.
        """
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

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

        # Mise à jour conditionnelle
        if "text" in update_data:
            review.text = review.validate_text(update_data["text"], "Text")

        if "rating" in update_data:
            review.rating = review.validate_rating(update_data["rating"],
                                                   "Rating")

        # Sauvegarde dans le repo
        self.review_repo.add(review)

        return review

    def delete_review(self, review_id):
        """
        Supprime un avis par son identifiant.
        Met aussi à jour la liste des reviews dans l’objet Place lié.
        Soulève une ValueError si la review est introuvable.
        """
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        # Nettoyage de la relation dans le Place concerné
        place = review.place
        if place and review in place.reviews:
            place.reviews.remove(review)
            self.place_repo.add(place)

        self.review_repo.delete(review_id)

    def get_reviews_by_user(self, user_id):
        """
        Retourne la liste des avis rédigés par un utilisateur donné.
        Soulève une erreur si l'utilisateur est introuvable.
        """
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        return [
            review for review in self.review_repo.get_all()
            if review.author and review.author.id == user_id
        ]

    def get_average_rating_for_place(self, place_id):
        """
        Calcule la moyenne des notes pour un lieu donné.
        Retourne None si aucun avis.
        """
        reviews = self.get_reviews_by_place(place_id)
        if not reviews:
            return None
        return sum(r.rating for r in reviews) / len(reviews)
