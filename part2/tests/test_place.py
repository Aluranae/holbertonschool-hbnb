import pytest
import time
from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


def test_create_valid_place():
    """
    Vérifie qu'une instance valide de Place peut être créée correctement.
    """
    owner = User(first_name="Han", last_name="Solo", email="han@falcon.space")
    place = Place(
        title="Cabine du Faucon",
        description="Un lieu mythique dans la galaxie.",
        price=500.0,
        latitude=12.34,
        longitude=56.78,
        owner=owner
    )

    # ✅ Vérifications
    assert isinstance(place, Place)
    assert place.title == "Cabine du Faucon"
    assert place.description == "Un lieu mythique dans la galaxie."
    assert place.price == 500.0
    assert place.latitude == 12.34
    assert place.longitude == 56.78
    assert place.owner == owner
    assert place.reviews == []
    assert place.amenities == []

    # 🖨️ Affichage complet
    print("\n✅ Création d'un logement réussie :")
    print(f"→ Titre : {place.title}")
    print(f"→ Description : {place.description}")
    print(f"→ Prix : {place.price}")
    print(f"→ Latitude : {place.latitude}")
    print(f"→ Longitude : {place.longitude}")
    print(f"→ Owner : {place.owner}")
    print(f"→ Reviews : {place.reviews}")
    print(f"→ Amenities : {place.amenities}")


def test_create_place_missing_required_fields():
    """
    Vérifie qu'une exception est levée si on tente de créer un Place
    sans titre, prix ou propriétaire.
    """
    owner = User(first_name="Lando", last_name="Calrissian", email="lando@cloud.city")

    # Manque le titre
    with pytest.raises(TypeError):
        Place(
            price=100.0,
            latitude=0.0,
            longitude=0.0,
            owner=owner
        )

    # Manque le prix
    with pytest.raises(TypeError):
        Place(
            title="Cloud City Loft",
            latitude=0.0,
            longitude=0.0,
            owner=owner
        )

    # Manque le owner
    with pytest.raises(TypeError):
        Place(
            title="Cloud City Loft",
            price=100.0,
            latitude=0.0,
            longitude=0.0
        )

    print("\n Exceptions correctement levées pour les champs manquants :")
    print("→ Erreur sans titre ✔")
    print("→ Erreur sans prix ✔")
    print("→ Erreur sans propriétaire ✔")


def test_create_place_with_empty_fields():
    """
    Vérifie qu'une erreur est levée si certains champs de Place sont vides ou None.
    """
    owner = User(first_name="Lando", last_name="Calrissian", email="lando@cloudcity.com")

    # Cas 1 : title vide → ValueError
    with pytest.raises(ValueError) as e1:
        Place(title="", description="Lieu chic", price=120.0, latitude=45.0, longitude=5.0, owner=owner)
    print("Erreur attendue (title vide) :", e1.value)

    # Cas 2 : title = None → TypeError
    with pytest.raises(TypeError) as e2:
        Place(title=None, description="Lieu chic", price=120.0, latitude=45.0, longitude=5.0, owner=owner)
    print("Erreur attendue (title None) :", e2.value)

    # Cas 3 : description vide → ValueError
    with pytest.raises(ValueError) as e3:
        Place(title="Cloud City", description="", price=120.0, latitude=45.0, longitude=5.0, owner=owner)
    print("Erreur attendue (description vide) :", e3.value)

    # Cas 4 : description = None → TypeError
    with pytest.raises(TypeError) as e4:
        Place(title="Cloud City", description=None, price=120.0, latitude=45.0, longitude=5.0, owner=owner)
    print("Erreur attendue (description None) :", e4.value)

    # Cas 5 : price = None → TypeError
    with pytest.raises(TypeError) as e5:
        Place(title="Cloud City", description="Ville flottante", price=None, latitude=45.0, longitude=5.0, owner=owner)
    print("Erreur attendue (price None) :", e5.value)


def test_create_place_with_non_string_title():
    """
    Vérifie qu'une TypeError est levée si title n'est pas une chaîne.
    """
    owner = User(first_name="Lando", last_name="Calrissian", email="lando@cloudcity.com")
    description = "Appartement perché"
    price = 120.0
    latitude = 45.0
    longitude = 5.0

    # Cas 1 : title est un entier
    with pytest.raises(TypeError) as e1:
        Place(title=123, description=description, price=price, latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (title = int) :", e1.value)

    # Cas 2 : title est un float
    with pytest.raises(TypeError) as e2:
        Place(title=4.5, description=description, price=price, latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (title = float) :", e2.value)

    # Cas 3 : title est une liste
    with pytest.raises(TypeError) as e3:
        Place(title=["Maison"], description=description, price=price, latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (title = list) :", e3.value)

    # Cas 4 : title est un booléen
    with pytest.raises(TypeError) as e4:
        Place(title=True, description=description, price=price, latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (title = bool) :", e4.value)


def test_create_place_with_title_too_long():
    """
    Vérifie qu'une ValueError est levée si le titre dépasse 100 caractères.
    """
    owner = User(first_name="Leia", last_name="Organa", email="leia@rebellion.org")
    description = "Palais luxueux dans les nuages"
    price = 250.0
    latitude = 42.5
    longitude = 3.2

    # Génère un titre de 101 caractères
    long_title = "L" * 101

    with pytest.raises(ValueError) as e:
        Place(
            title=long_title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )

    print("Erreur attendue (title > 100 caractères) :", e.value)


def test_create_place_with_invalid_price_value():
    """
    Vérifie qu'une ValueError est levée si price est 0 ou négatif.
    """
    owner = User(first_name="Han", last_name="Solo", email="han@falcon.co")
    title = "Appartement Corellien"
    description = "Avec vue sur les chantiers orbitaux"
    latitude = 44.0
    longitude = 1.5

    # Cas 1 : price = 0
    with pytest.raises(ValueError) as e1:
        Place(title=title, description=description, price=0, latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (price = 0) :", e1.value)

    # Cas 2 : price = -10
    with pytest.raises(ValueError) as e2:
        Place(title=title, description=description, price=-10, latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (price < 0) :", e2.value)


def test_create_place_with_invalid_latitude():
    """
    Vérifie qu'une ValueError est levée si latitude est hors de l'intervalle [-90, 90].
    """
    owner = User(first_name="Padmé", last_name="Amidala", email="padme@naboo.gov")
    title = "Villa lacustre"
    description = "Située sur les lacs de Naboo"
    price = 300.0
    longitude = 6.6

    # Cas 1 : latitude > 90
    with pytest.raises(ValueError) as e1:
        Place(title=title, description=description, price=price, latitude=91.0, longitude=longitude, owner=owner)
    print("Erreur attendue (latitude > 90) :", e1.value)

    # Cas 2 : latitude < -90
    with pytest.raises(ValueError) as e2:
        Place(title=title, description=description, price=price, latitude=-91.0, longitude=longitude, owner=owner)
    print("Erreur attendue (latitude < -90) :", e2.value)


def test_create_place_with_invalid_longitude():
    """
    Vérifie qu'une ValueError est levée si longitude est hors de l'intervalle [-180, 180].
    """
    owner = User(first_name="Bail", last_name="Organa", email="bail@alderaan.gov")
    title = "Domaine royal"
    description = "Résidence de la famille Organa"
    price = 400.0
    latitude = 47.2

    # Cas 1 : longitude > 180
    with pytest.raises(ValueError) as e1:
        Place(title=title, description=description, price=price, latitude=latitude, longitude=181.0, owner=owner)
    print("Erreur attendue (longitude > 180) :", e1.value)

    # Cas 2 : longitude < -180
    with pytest.raises(ValueError) as e2:
        Place(title=title, description=description, price=price, latitude=latitude, longitude=-181.0, owner=owner)
    print("Erreur attendue (longitude < -180) :", e2.value)


def test_create_place_with_invalid_owner():
    """
    Vérifie qu'une TypeError est levée si owner n'est pas une instance de User.
    """
    title = "Caserne des clones"
    description = "Située sur Kamino"
    price = 500.0
    latitude = -33.0
    longitude = 151.0

    # Cas 1 : owner = string
    with pytest.raises(TypeError) as e1:
        Place(title=title, description=description, price=price, latitude=latitude, longitude=longitude, owner="not_a_user")
    print("Erreur attendue (owner = str) :", e1.value)

    # Cas 2 : owner = int
    with pytest.raises(TypeError) as e2:
        Place(title=title, description=description, price=price, latitude=latitude, longitude=longitude, owner=42)
    print("Erreur attendue (owner = int) :", e2.value)

    # Cas 3 : owner = float
    with pytest.raises(TypeError) as e3:
        Place(title=title, description=description, price=price, latitude=latitude, longitude=longitude, owner=3.14)
    print("Erreur attendue (owner = float) :", e3.value)

    # Cas 4 : owner = None
    with pytest.raises(TypeError) as e4:
        Place(title=title, description=description, price=price, latitude=latitude, longitude=longitude, owner=None)
    print("Erreur attendue (owner = None) :", e4.value)

    # Cas 5 : owner = dict
    with pytest.raises(TypeError) as e5:
        Place(title=title, description=description, price=price, latitude=latitude, longitude=longitude, owner={"id": "abc"})
    print("Erreur attendue (owner = dict) :", e5.value)


def test_create_place_with_invalid_lat_or_long_type():
    """
    Vérifie qu'une TypeError est levée si latitude ou longitude ne sont pas des float.
    """
    owner = User(first_name="Obi-Wan", last_name="Kenobi", email="kenobi@jedi.org")
    title = "Refuge sur Tatooine"
    description = "Lieu tenu secret"
    price = 100.0

    # Cas latitude : string
    with pytest.raises(TypeError) as e1:
        Place(title=title, description=description, price=price, latitude="34.0", longitude=12.0, owner=owner)
    print("Erreur attendue (latitude = str) :", e1.value)

    # Cas latitude : int
    with pytest.raises(TypeError) as e2:
        Place(title=title, description=description, price=price, latitude=34, longitude=12.0, owner=owner)
    print("Erreur attendue (latitude = int) :", e2.value)

    # Cas longitude : string
    with pytest.raises(TypeError) as e3:
        Place(title=title, description=description, price=price, latitude=34.0, longitude="12.0", owner=owner)
    print("Erreur attendue (longitude = str) :", e3.value)

    # Cas longitude : int
    with pytest.raises(TypeError) as e4:
        Place(title=title, description=description, price=price, latitude=34.0, longitude=12, owner=owner)
    print("Erreur attendue (longitude = int) :", e4.value)


def test_create_place_with_invalid_price_type():
    """
    Vérifie qu'une TypeError est levée si price n'est pas un float ou un int.
    """
    owner = User(first_name="Mace", last_name="Windu", email="windu@council.jedi")
    title = "Tour du Temple"
    description = "Niveau 5, aile ouest"
    latitude = 34.0
    longitude = 18.0

    # Cas 1 : price = string
    with pytest.raises(TypeError) as e1:
        Place(title=title, description=description, price="200", latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (price = str) :", e1.value)

    # Cas 2 : price = list
    with pytest.raises(TypeError) as e2:
        Place(title=title, description=description, price=[200], latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (price = list) :", e2.value)

    # Cas 3 : price = None
    with pytest.raises(TypeError) as e3:
        Place(title=title, description=description, price=None, latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (price = None) :", e3.value)

    # Cas 4 : price = bool
    with pytest.raises(TypeError) as e4:
        Place(title=title, description=description, price=True, latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (price = bool) :", e4.value)

    # Cas 5 : price = dict
    with pytest.raises(TypeError) as e5:
        Place(title=title, description=description, price={"value": 200}, latitude=latitude, longitude=longitude, owner=owner)
    print("Erreur attendue (price = dict) :", e5.value)


def test_update_place_with_invalid_title_type():
    """
    Vérifie qu'une TypeError est levée si on met à jour title avec un type non str.
    """
    owner = User(first_name="Ahsoka", last_name="Tano", email="ahsoka@fulcrum.org")
    place = Place(
        title="Temple Jedi",
        description="Lieu d'entraînement mystique",
        price=180.0,
        latitude=40.0,
        longitude=10.0,
        owner=owner
    )

    # Cas 1 : title = int
    with pytest.raises(TypeError) as e1:
        place.update(title=123)
    print("Erreur attendue (update title = int) :", e1.value)

    # Cas 2 : title = float
    with pytest.raises(TypeError) as e2:
        place.update(title=3.14)
    print("Erreur attendue (update title = float) :", e2.value)

    # Cas 3 : title = list
    with pytest.raises(TypeError) as e3:
        place.update(title=["Maison de repos"])
    print("Erreur attendue (update title = list) :", e3.value)

    # Cas 4 : title = None
    with pytest.raises(TypeError) as e4:
        place.update(title=None)
    print("Erreur attendue (update title = None) :", e4.value)


def test_place_repr_format():
    """
    Vérifie que __repr__ retourne une chaîne du type : <Place id: title>
    """
    owner = User(first_name="Mon", last_name="Mothma", email="mon@mothma.org")
    place = Place(
        title="Base Rebelle",
        description="Lieu secret sur Yavin 4",
        price=200.0,
        latitude=25.0,
        longitude=13.3,
        owner=owner
    )

    result = repr(place)
    print("Sortie de __repr__() :", result)

    assert isinstance(result, str)
    assert result.startswith("<Place ")
    assert place.id in result
    assert place.title in result


def test_place_str_format():
    """
    Vérifie que __str__ retourne une chaîne lisible contenant les infos clés du lieu.
    """
    owner = User(first_name="Obi-Wan", last_name="Kenobi", email="kenobi@jedi.org")
    place = Place(
        title="Temple Jedi",
        description="Lieu sacré",
        price=300.0,
        latitude=40.0,
        longitude=10.0,
        owner=owner
    )

    result = str(place)
    print("Sortie de __str__() :\n", result)

    assert isinstance(result, str)
    assert "[Place]" in result
    assert place.title in result
    assert str(place.price) in result
    assert str(place.latitude) in result
    assert str(place.longitude) in result
    assert owner.first_name in result
    assert owner.last_name in result
    assert owner.email in result


def test_place_update_modifies_attributes():
    """
    Vérifie que update() modifie les champs existants avec des valeurs valides.
    """
    owner = User(first_name="Jyn", last_name="Erso", email="jyn@rebellion.org")
    place = Place(
        title="Cache rebelle",
        description="Ancien entrepôt de la Résistance",
        price=150.0,
        latitude=44.0,
        longitude=6.0,
        owner=owner
    )

    # Mise à jour des champs valides
    place.update(
        title="QG temporaire",
        description="Base secrète sur Scarif",
        price=200.0,
        latitude=45.5,
        longitude=7.5
    )

    # Affichage après modification
    print("Place après update :")
    print("title      :", place.title)
    print("description:", place.description)
    print("price      :", place.price)
    print("latitude   :", place.latitude)
    print("longitude  :", place.longitude)

    # Vérifications
    assert place.title == "QG temporaire"
    assert place.description == "Base secrète sur Scarif"
    assert place.price == 200.0
    assert place.latitude == 45.5
    assert place.longitude == 7.5


def test_update_place_ignores_unknown_keys():
    """
    Vérifie que update() ignore les clés inconnues sans lever d'exception.
    """
    owner = User(first_name="Lando", last_name="Calrissian", email="lando@bespin.org")
    place = Place(
        title="Refuge du contrebandier",
        description="Niché dans les nuages",
        price=500.0,
        latitude=12.0,
        longitude=34.0,
        owner=owner
    )

    print("Avant update :")
    print("title :", place.title)
    print("hasattr(place, 'categorie') :", hasattr(place, "categorie"))
    print("hasattr(place, 'climatiseur') :", hasattr(place, "climatiseur"))

    # Mise à jour avec des clés inconnues
    place.update(categorie="haut standing", climatiseur=True)

    print("\nAprès update avec clés inconnues :")
    print("title :", place.title)
    print("hasattr(place, 'categorie') :", hasattr(place, "categorie"))
    print("hasattr(place, 'climatiseur') :", hasattr(place, "climatiseur"))

    # Vérifications
    assert not hasattr(place, "categorie")
    assert not hasattr(place, "climatiseur")
    assert place.title == "Refuge du contrebandier"


def test_update_place_with_invalid_value_types():
    """
    Vérifie qu'une exception est levée si update() reçoit des valeurs de type incorrect.
    """
    owner = User(first_name="Boba", last_name="Fett", email="boba@slave1.com")
    place = Place(
        title="Chambre froide",
        description="Parfait pour stocker des primes",
        price=750.0,
        latitude=40.0,
        longitude=8.0,
        owner=owner
    )

    print("Avant update :")
    print("title :", place.title)
    print("price :", place.price)

    # Cas 1 : title est un entier
    try:
        place.update(title=12345)
    except Exception as e:
        print("\nException attendue pour title (int) :", type(e).__name__, "-", e)

    # Cas 2 : price est une chaîne
    try:
        place.update(price="gratuit")
    except Exception as e:
        print("\nException attendue pour price (str) :", type(e).__name__, "-", e)

    # Vérifie que les données n'ont pas été altérées
    assert place.title == "Chambre froide"
    assert place.price == 750.0


def test_place_identity_and_equality_same_instance():
    """
    Test 18 – Deux objets identiques (même instance) sont égaux :
    Vérifie que deux variables pointant vers le même objet Place sont
    à la fois égales (==) et identiques (is).
    """
    owner = User(first_name="Cassian", last_name="Andor", email="cassian@rebellion.org")
    place = Place(
        title="Refuge secret",
        description="Abri en zone isolée",
        price=120.0,
        latitude=42.0,
        longitude=5.0,
        owner=owner
    )

    # Création d’une seconde référence pointant vers le même objet
    same_place = place

    print("=== Affichage des deux références ===")
    print(f"place id: {id(place)}")
    print(f"same_place id: {id(same_place)}")

    # Vérifie identité mémoire
    assert same_place is place, "Les deux références devraient pointer vers le même objet"

    # Vérifie égalité logique
    assert same_place == place, "Les deux objets devraient être considérés comme égaux"


def test_place_equality_same_id_different_objects():
    """
    Test 19 – Deux objets différents avec le même id sont considérés égaux.
    Vérifie que la méthode __eq__ fonctionne selon l’ID logique, même si ce
    sont des instances distinctes en mémoire.
    """
    owner1 = User(first_name="Saw", last_name="Gerrera", email="saw@partisans.org")
    owner2 = User(first_name="Saw", last_name="Gerrera", email="saw@partisans.org")

    # Création de deux objets différents
    place1 = Place(
        title="Caverne de Jedha",
        description="Cache secrète des Partisans",
        price=90.0,
        latitude=33.5,
        longitude=35.5,
        owner=owner1
    )

    place2 = Place(
        title="Caverne clonée",
        description="Même lieu, autre objet",
        price=90.0,
        latitude=33.5,
        longitude=35.5,
        owner=owner2
    )

    # On force manuellement le même id
    place2._id = place1.id

    print("=== Comparaison logique ===")
    print(f"place1 id : {id(place1)} / place1 UUID : {place1.id}")
    print(f"place2 id : {id(place2)} / place2 UUID : {place2.id}")

    # Ils ne sont pas identiques (pas la même instance)
    assert place1 is not place2, "Ce sont deux objets différents"

    # Mais ils doivent être égaux car id est identique
    assert place1 == place2, "__eq__ doit retourner True si les id sont égaux"


def test_place_owner_is_user():
    """
    Test 20 – Le propriétaire est bien un objet User.
    Vérifie que la relation Place → User est correctement initialisée.
    """
    owner = User(first_name="Cassian", last_name="Andor", email="cassian@rebellion.org")

    place = Place(
        title="Cache de Ferrix",
        description="Appartement discret près du marché",
        price=180.0,
        latitude=48.9,
        longitude=2.4,
        owner=owner
    )

    print("=== Vérification de la relation Place → User ===")
    print(f"Type de owner : {type(place.owner)}")
    print(f"Prénom : {place.owner.first_name}")
    print(f"Nom : {place.owner.last_name}")
    print(f"Email : {place.owner.email}")

    assert isinstance(place.owner, User), "Le propriétaire doit être un objet User"
    assert place.owner.first_name == "Cassian"
    assert place.owner.last_name == "Andor"
    assert place.owner.email == "cassian@rebellion.org"


def test_place_accepts_multiple_reviews():
    owner = User(first_name="Mon", last_name="Mothma", email="mon@senat.org")
    author1 = User(first_name="Bail", last_name="Organa", email="bail@alderaan.org")
    author2 = User(first_name="Leia", last_name="Organa", email="leia@rebellion.org")

    place = Place(
        title="Résidence secrète",
        description="Appartement de soutien à la Rébellion",
        price=400.0,
        latitude=50.0,
        longitude=4.0,
        owner=owner
    )

    review1 = Review(text="Excellent lieu stratégique", rating=5, author=author1, place=place)
    review2 = Review(text="Confort et discrétion", rating=4, author=author2, place=place)

    print("=== Reviews liés au Place ===")
    for i, r in enumerate(place.reviews, start=1):
        print(f"Review {i} – {r.text} par {r.author.first_name}")

    assert len(place.reviews) == 2
    assert review1 in place.reviews
    assert review2 in place.reviews


def test_place_accepts_multiple_amenities():
    """
    Test 22 – Ajout de plusieurs Amenity à un Place.
    Vérifie que Place.amenities accepte plusieurs objets Amenity.
    """
    owner = User(first_name="Padmé", last_name="Naberrie", email="padme@senat.org")

    place = Place(
        title="Villa de Theed",
        description="Résidence sécurisée avec vue sur les cascades",
        price=900.0,
        latitude=31.2,
        longitude=35.6,
        owner=owner
    )

    amenity1 = Amenity(name="Holo-net")
    amenity2 = Amenity(name="Bacta Tank privé")

    place.add_amenity(amenity1)
    place.add_amenity(amenity2)

    print("\n=== DEBUG Place.amenities ===")
    print(f"Type de place.amenities : {type(place.amenities)}")
    print(f"Longueur de la liste : {len(place.amenities)}")
    for idx, a in enumerate(place.amenities, start=1):
        print(f"Amenity {idx} : id={a.id} | name={a.name} | type={type(a)}")
    print("=== FIN DEBUG ===\n")

    assert len(place.amenities) == 2, "Le lieu devrait avoir 2 commodités"
    assert place.amenities[0] == amenity1
    assert place.amenities[1] == amenity2
