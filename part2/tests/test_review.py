import pytest
import time
from datetime import datetime
from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


def test_create_valid_review():
    """
    R1. Vérifie qu’un Review valide peut être créé sans erreur,
    et que ses attributs sont correctement initialisés.
    """
    # Création d'un utilisateur et d'un lieu
    user = User(first_name="Leia", last_name="Organa", email="leia@rebellion.org")
    place = Place(
        title="Base Echo",
        description="Refuge sur Hoth",
        price=80,
        owner=user,
        latitude=60.0,
        longitude=-44.0
    )

    # Création d’un avis valide
    review = Review(
        text="Lieu glacial mais sécurisé, parfait pour une retraite.",
        rating=4,
        author=user,
        place=place
    )

    # Affichages pour suivi visuel
    print("Review créé :", review)
    print("ID Review :", review.id)
    print("Text :", review.text)
    print("Rating :", review.rating)
    print("Author ID :", review.author.id)
    print("Place title :", review.place.title)
    print("Date de création :", review.created_at)
    print("Date de mise à jour :", review.updated_at)

    # Assertions
    assert isinstance(review, Review)
    assert review.text == "Lieu glacial mais sécurisé, parfait pour une retraite."
    assert review.rating == 4
    assert review.author == user
    assert review.place == place
    assert review.id is not None
    assert review.created_at is not None
    assert review.updated_at is not None


def test_repr_contains_expected_info():
    """
    R2. Vérifie que le format de __repr__() contient bien l’ID du review,
    la note et l’ID de l’auteur.
    """
    # Création des objets nécessaires
    user = User(first_name="Han", last_name="Solo", email="han@falcon.space")
    place = Place(
        title="Cantina Mos Eisley",
        description="Bar très fréquenté par des contrebandiers",
        price=30,
        owner=user,
        latitude=25.5,
        longitude=37.8
    )

    review = Review(
        text="Ambiance intergalactique garantie.",
        rating=5,
        author=user,
        place=place
    )

    # Appel à __repr__
    repr_str = repr(review)

    # Affichage pour la console
    print("Résultat de repr(review) :", repr_str)

    # Vérifications
    assert isinstance(repr_str, str)
    assert review.id in repr_str
    assert f"rating={review.rating}" in repr_str
    assert review.author.id in repr_str


def test_str_returns_readable_format():
    """
    R3. Vérifie que le format renvoyé par __str__() est lisible,
    et contient bien le nom complet de l’auteur, le titre du lieu,
    la note et le texte de l’avis.
    """
    # Création d’un utilisateur et d’un lieu
    user = User(first_name="Obi-Wan", last_name="Kenobi", email="obiwan@jedi.org")
    place = Place(
        title="Tatooine Refuge",
        description="Une cachette dans le désert",
        price=15,
        owner=user,
        latitude=33.0,
        longitude=12.0
    )

    # Création de l'avis
    review = Review(
        text="Endroit calme pour méditer, malgré les tempêtes de sable.",
        rating=5,
        author=user,
        place=place
    )

    # Appel à str()
    str_output = str(review)

    # Affichage pour vérification
    print("Résultat de str(review) :", str_output)

    # Vérification des composants clés dans la sortie
    assert isinstance(str_output, str)
    assert "Obi-Wan Kenobi" in str_output
    assert "Tatooine Refuge" in str_output
    assert "5⭐" in str_output
    assert "Endroit calme pour méditer" in str_output


def test_missing_text_raises_error():
    """
    R4. Vérifie qu'une TypeError est levée si l'on oublie le champ 'text'
    lors de la création d’un Review.
    """
    user = User(first_name="Padmé", last_name="Amidala", email="padme@naboo.gal")
    place = Place(
        title="Palais de Theed",
        description="Lieu royal élégant",
        price=120,
        owner=user,
        latitude=45.2,
        longitude=19.3
    )

    # Tentative de création sans 'text'
    with pytest.raises(TypeError) as excinfo:
        review = Review(
            rating=4,
            author=user,
            place=place
        )

    # Affichage du message d’erreur pour vérification
    print("Message d’erreur :", str(excinfo.value))

    assert "missing 1 required positional argument: 'text'" in str(excinfo.value)


def test_missing_rating_raises_error():
    """
    R5. Vérifie qu'une TypeError est levée si l'on oublie le champ 'rating'
    lors de la création d’un Review.
    """
    user = User(first_name="Lando", last_name="Calrissian", email="lando@bespin.gov")
    place = Place(
        title="Cloud City",
        description="Station flottante au-dessus de Bespin",
        price=200,
        owner=user,
        latitude=28.0,
        longitude=-90.0
    )

    # Tentative de création sans 'rating'
    with pytest.raises(TypeError) as excinfo:
        review = Review(
            text="Vue imprenable sur les nuages.",
            author=user,
            place=place
        )

    # Affichage du message d’erreur pour vérification
    print("Message d’erreur :", str(excinfo.value))

    assert "missing 1 required positional argument: 'rating'" in str(excinfo.value)


def test_missing_author_raises_error():
    """
    R6. Vérifie qu'une TypeError est levée si l'on oublie le champ 'author'
    lors de la création d’un Review.
    """
    user = User(first_name="Qui-Gon", last_name="Jinn", email="quigon@jedi.org")
    place = Place(
        title="Auberge de Tython",
        description="Lieu d’étude de la Force",
        price=50,
        owner=user,
        latitude=41.3,
        longitude=23.7
    )

    # Tentative de création sans 'author'
    with pytest.raises(TypeError) as excinfo:
        review = Review(
            text="Parfait pour méditer en paix.",
            rating=5,
            place=place
        )

    # Affichage du message d’erreur
    print("Message d’erreur :", str(excinfo.value))

    assert "missing 1 required positional argument: 'author'" in str(excinfo.value)


def test_missing_place_raises_error():
    """
    R7. Vérifie qu'une TypeError est levée si l'on oublie le champ 'place'
    lors de la création d’un Review.
    """
    user = User(first_name="Ahsoka", last_name="Tano", email="ahsoka@togruta.net")
    # Un lieu est quand même créé pour l’attribut owner, mais non utilisé
    dummy_place = Place(
        title="Temple de Coruscant",
        description="Ancien bastion Jedi",
        price=1,
        owner=user,
        latitude=0.0,
        longitude=0.0
    )

    # Tentative de création sans 'place'
    with pytest.raises(TypeError) as excinfo:
        review = Review(
            text="Lieu chargé en histoire.",
            rating=5,
            author=user
        )

    # Affichage du message d’erreur
    print("Message d’erreur :", str(excinfo.value))

    assert "missing 1 required positional argument: 'place'" in str(excinfo.value)


def test_text_must_be_string():
    """
    R8. Vérifie qu'une TypeError est levée si 'text' n'est pas une string.
    """
    user = User(first_name="Bo-Katan", last_name="Kryze", email="bokatan@mandalore.org")
    place = Place(
        title="Dôme de Sundari",
        description="Ville protégée par une coupole",
        price=150,
        owner=user,
        latitude=70.2,
        longitude=40.9
    )

    with pytest.raises(TypeError) as excinfo:
        review = Review(
            text=12345,  # ❌ entier au lieu de str
            rating=4,
            author=user,
            place=place
        )

    print("Message d’erreur :", str(excinfo.value))
    assert "Text must be a string" in str(excinfo.value)


def test_text_cannot_be_empty():
    """
    R9. Vérifie qu'une ValueError est levée si 'text' est une chaîne vide.
    """
    user = User(first_name="Yoda", last_name="Mystery", email="yoda@dagobah.system")
    place = Place(
        title="Marais de Dagobah",
        description="Retraite d’un maître Jedi",
        price=20,
        owner=user,
        latitude=12.4,
        longitude=5.6
    )

    with pytest.raises(ValueError) as excinfo:
        review = Review(
            text="",
            rating=5,
            author=user,
            place=place
        )

    print("Message d’erreur :", str(excinfo.value))
    assert "Text is required" in str(excinfo.value)


def test_text_stripped_empty():
    """
    R10. Vérifie qu'une ValueError est levée si 'text' contient uniquement des espaces.
    """
    user = User(first_name="Cal", last_name="Kestis", email="cal@jedifallen.com")
    place = Place(
        title="Méditation sur Zeffo",
        description="Ancien tombeau céleste",
        price=70,
        owner=user,
        latitude=49.5,
        longitude=11.0
    )

    with pytest.raises(ValueError) as excinfo:
        review = Review(
            text="   ",  # ❌ espaces uniquement
            rating=4,
            author=user,
            place=place
        )

    print("Message d’erreur :", str(excinfo.value))
    assert "Text is required" in str(excinfo.value)


def test_text_too_long():
    """
    R11. Vérifie qu'une ValueError est levée si 'text' dépasse 500 caractères.
    """
    user = User(first_name="Cassian", last_name="Andor", email="andor@rebellion.net")
    place = Place(
        title="Base sur Ferrix",
        description="Avant-poste rebelle discret",
        price=45,
        owner=user,
        latitude=21.4,
        longitude=6.7
    )

    # Génération d'un texte de 501 caractères
    long_text = "X" * 501

    with pytest.raises(ValueError) as excinfo:
        review = Review(
            text=long_text,
            rating=3,
            author=user,
            place=place
        )

    print("Message d’erreur :", str(excinfo.value))
    assert "Text must be at most 500 characters" in str(excinfo.value)


def test_text_exactly_500_characters():
    """
    R12. Vérifie qu’un Review peut être créé avec un texte de 500 caractères pile.
    """
    user = User(first_name="Saw", last_name="Gerrera", email="saw@onderon.rebel")
    place = Place(
        title="Cave de Jedha",
        description="Refuge des extrémistes rebelles",
        price=30,
        owner=user,
        latitude=34.2,
        longitude=15.8
    )

    # Texte de 500 caractères
    valid_text = "X" * 500

    review = Review(
        text=valid_text,
        rating=2,
        author=user,
        place=place
    )

    # Affichage pour vérification
    print("Longueur du texte :", len(review.text))
    print("Review créé :", review)

    assert len(review.text) == 500
    assert review.text == valid_text


def test_rating_must_be_int():
    """
    R13. Vérifie qu'une TypeError est levée si 'rating' n’est pas un entier.
    """
    user = User(first_name="Jyn", last_name="Erso", email="jyn@scarif.rebel")
    place = Place(
        title="Base secrète de Scarif",
        description="Planète archiviste de l’Empire",
        price=60,
        owner=user,
        latitude=11.2,
        longitude=29.1
    )

    # Test avec une chaîne
    with pytest.raises(TypeError) as excinfo1:
        Review(
            text="Planète dangereuse mais belle.",
            rating="5",  # ❌ string
            author=user,
            place=place
        )
    print("Erreur rating='5' :", str(excinfo1.value))
    assert "Rating must be an integer" in str(excinfo1.value)

    # Test avec un float
    with pytest.raises(TypeError) as excinfo2:
        Review(
            text="Architecture impressionnante.",
            rating=4.5,  # ❌ float
            author=user,
            place=place
        )
    print("Erreur rating=4.5 :", str(excinfo2.value))
    assert "Rating must be an integer" in str(excinfo2.value)


def test_rating_too_low():
    """
    R14. Vérifie qu'une ValueError est levée si 'rating' est inférieur à 1.
    """
    user = User(first_name="Hera", last_name="Syndulla", email="hera@ghost.net")
    place = Place(
        title="Phare de Lothal",
        description="Poste d’observation rebelle",
        price=55,
        owner=user,
        latitude=10.0,
        longitude=18.0
    )

    with pytest.raises(ValueError) as excinfo:
        review = Review(
            text="Rien à signaler. Vue dégagée.",
            rating=0,  # ❌ trop bas
            author=user,
            place=place
        )

    print("Message d’erreur :", str(excinfo.value))
    assert "Rating must be between 1 and 5" in str(excinfo.value)

def test_rating_too_high():
    """
    R15. Vérifie qu'une ValueError est levée si 'rating' est supérieur à 5.
    """
    user = User(first_name="Kanan", last_name="Jarrus", email="kanan@jedi.ghost")
    place = Place(
        title="Ruines de Malachor",
        description="Temple Sith ancien",
        price=90,
        owner=user,
        latitude=3.3,
        longitude=66.6
    )

    with pytest.raises(ValueError) as excinfo:
        review = Review(
            text="Étrange mais fascinant.",
            rating=6,  # ❌ trop élevé
            author=user,
            place=place
        )

    print("Message d’erreur :", str(excinfo.value))
    assert "Rating must be between 1 and 5" in str(excinfo.value)


def test_rating_bounds_valid():
    """
    R16. Vérifie que les valeurs limites de rating (1 et 5) sont valides.
    """
    user = User(first_name="Ezra", last_name="Bridger", email="ezra@lothal.net")
    place = Place(
        title="Tour d'observation de Lothal",
        description="Point stratégique sur Lothal",
        price=40,
        owner=user,
        latitude=17.2,
        longitude=12.6
    )

    # Cas rating = 1
    review_low = Review(
        text="Expérience moyenne, mais correcte.",
        rating=1,
        author=user,
        place=place
    )
    print("Review avec rating=1 :", review_low)

    # Cas rating = 5
    review_high = Review(
        text="Expérience incroyable, je recommande !",
        rating=5,
        author=user,
        place=place
    )
    print("Review avec rating=5 :", review_high)

    # Assertions
    assert review_low.rating == 1
    assert review_high.rating == 5


def test_author_must_be_User_instance():
    """
    R17. Vérifie qu'une TypeError est levée si 'author' n’est pas une instance de User.
    """
    user = User(first_name="Thrawn", last_name="Mitth", email="thrawn@empire.gov")
    place = Place(
        title="Croiseur Chimaera",
        description="Navire de commandement impérial",
        price=250,
        owner=user,
        latitude=73.2,
        longitude=42.1
    )

    # Test avec une string au lieu d’un User
    with pytest.raises(TypeError) as excinfo:
        Review(
            text="Organisation tactique impressionnante.",
            rating=5,
            author="NotAUser",  # ❌ pas un User
            place=place
        )

    print("Message d’erreur :", str(excinfo.value))
    assert "Author must be an instance of User" in str(excinfo.value)


def test_author_can_be_used_in_repr():
    """
    R18. Vérifie que l’ID de l’auteur est présent dans le __repr__ du Review.
    """
    user = User(first_name="Bail", last_name="Organa", email="bail@alderaan.gov")
    place = Place(
        title="Palais d’Alderaan",
        description="Demeure royale de la famille Organa",
        price=180,
        owner=user,
        latitude=44.4,
        longitude=12.1
    )

    review = Review(
        text="Une splendeur architecturale.",
        rating=5,
        author=user,
        place=place
    )

    repr_output = repr(review)
    print("Sortie de __repr__ :", repr_output)

    assert user.id in repr_output
    assert f"rating={review.rating}" in repr_output


def test_place_must_be_Place_instance():
    """
    R19. Vérifie qu'une TypeError est levée si 'place' n’est pas une instance de Place.
    """
    user = User(first_name="Mon", last_name="Mothma", email="mon@senate.rep")

    with pytest.raises(TypeError) as excinfo:
        Review(
            text="Endroit symbolique de la rébellion.",
            rating=5,
            author=user,
            place="NotAPlace"  # ❌ chaîne au lieu d’un objet Place
        )

    print("Message d’erreur :", str(excinfo.value))
    assert "Place must be an instance of Place" in str(excinfo.value)


def test_multiple_reviews_same_author_place():
    """
    R20. Vérifie qu’on peut créer plusieurs Review avec le même auteur et le même lieu.
    """
    user = User(first_name="Din", last_name="Djarin", email="mando@navarro.system")
    place = Place(
        title="Forge Mandalorienne",
        description="Lieu sacré des armuriers",
        price=100,
        owner=user,
        latitude=81.0,
        longitude=33.0
    )

    # Premier avis
    review1 = Review(
        text="Une expérience digne des légendes mandaloriennes.",
        rating=5,
        author=user,
        place=place
    )

    # Deuxième avis sur le même lieu par la même personne
    review2 = Review(
        text="Après plusieurs jours, toujours aussi impressionné.",
        rating=4,
        author=user,
        place=place
    )

    print("Review 1 :", review1)
    print("Review 2 :", review2)

    # Vérifications
    assert isinstance(review1, Review)
    assert isinstance(review2, Review)
    assert review1 is not review2
    assert review1.author == review2.author
    assert review1.place == review2.place
    assert review1.text != review2.text


def test_reviews_can_have_same_text_different_rating():
    """
    R21. Vérifie qu’on peut créer deux Review avec le même texte,
    mais des notes différentes (et/ou auteur/place différents).
    """
    user1 = User(first_name="Tech", last_name="CloneForce99", email="tech@badbatch.org")
    user2 = User(first_name="Echo", last_name="CloneForce99", email="echo@badbatch.org")

    place = Place(
        title="Vaisseau Marauder",
        description="Transport modifié du Bad Batch",
        price=70,
        owner=user1,
        latitude=60.0,
        longitude=42.0
    )

    text = "Parfait pour des missions discrètes."

    # Deux Review avec même texte, mais auteurs/notes différentes
    review1 = Review(text=text, rating=5, author=user1, place=place)
    review2 = Review(text=text, rating=3, author=user2, place=place)

    print("Review 1 :", review1)
    print("Review 2 :", review2)

    # Vérifications
    assert review1.text == review2.text
    assert review1.rating != review2.rating
    assert review1.author != review2.author


def test_review_creation_establishes_bidirectional_links():
    """
    Vérifie que la création d'un Review établit automatiquement les liens
    avec l'utilisateur (User.reviews) et le lieu (Place.reviews).
    """
    # Création d'un utilisateur
    user = User(first_name="Obi-Wan", last_name="Kenobi", email="obiwan@jedi.org")

    # Création d'un lieu
    place = Place(
        title="Cabane sur Tatooine",
        description="Modeste refuge dans le désert",
        price=15.0,
        latitude=23.5,
        longitude=45.1,
        owner=user
    )

    # Création d'un avis
    review = Review(
        text="Endroit très calme, parfait pour méditer.",
        rating=5,
        author=user,
        place=place
    )

    # Vérification des relations automatiques
    assert review in user.reviews
    assert review in place.reviews
