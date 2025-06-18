import pytest
import time
from datetime import datetime
from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


def test_create_valid_amenity():
    """
    Vérifie qu’un Amenity valide peut être créé sans erreur,
    et que tous les attributs sont correctement initialisés.
    """

    print(">>> Création d’un Amenity valide avec name = 'Wi-Fi'")
    amenity = Amenity(name="Wi-Fi")

    print(">>> Objet créé :", amenity)

    print(">>> Attributs hérités :")
    print("- id =", amenity.id)
    print("- created_at =", amenity.created_at)
    print("- updated_at =", amenity.updated_at)

    print(">>> Attribut spécifique :")
    print("- name =", amenity.name)

    print(">>> Test des méthodes d’affichage :")
    print("- repr() :", repr(amenity))
    print("- str()  :", str(amenity))

    assert isinstance(amenity, Amenity)
    assert isinstance(amenity.id, str)
    assert isinstance(amenity.created_at, datetime)
    assert isinstance(amenity.updated_at, datetime)
    assert amenity.name == "Wi-Fi"


def test_create_amenity_without_name():
    """
    Vérifie qu’une exception TypeError est levée si aucun nom n’est fourni.
    """

    print(">>> Tentative de création d’un Amenity sans passer de name...")

    with pytest.raises(TypeError) as exc_info:
        amenity = Amenity()  # Pas de name fourni

    print(">>> Exception capturée :", exc_info.value)


def test_create_amenity_with_empty_name():
    """
    Vérifie qu'une ValueError est levée si le nom est vide
    ou uniquement composé d'espaces.
    """

    print(">>> Tentative avec une chaîne vide : Amenity('')")
    with pytest.raises(ValueError) as exc1:
        Amenity("")

    print(">>> Exception capturée :", exc1.value)

    print(">>> Tentative avec une chaîne d'espaces : Amenity('   ')")
    with pytest.raises(ValueError) as exc2:
        Amenity("   ")

    print(">>> Exception capturée :", exc2.value)


def test_create_amenity_with_non_string_name():
    """
    Vérifie qu'une TypeError est levée si le nom n'est pas une chaîne de caractères.
    """

    invalid_values = [42, None, [], {}]

    for value in invalid_values:
        print(f">>> Tentative de création avec name = {repr(value)} (type {type(value).__name__})")
        with pytest.raises(TypeError) as exc_info:
            Amenity(value)
        print(">>> Exception capturée :", exc_info.value)


def test_create_amenity_with_too_long_name():
    """
    Vérifie qu'une ValueError est levée si le nom dépasse 50 caractères.
    """

    long_name = "x" * 51  # 51 caractères

    print(f">>> Tentative avec un nom de {len(long_name)} caractères")
    with pytest.raises(ValueError) as exc_info:
        Amenity(long_name)

    print(">>> Exception capturée :", exc_info.value)


def test_repr_method_of_amenity():
    """
    Vérifie que __repr__() retourne une chaîne formatée avec id et name.
    """

    print(">>> Création d’un Amenity pour tester __repr__()")
    amenity = Amenity("Jacuzzi")
    repr_output = repr(amenity)

    print(">>> Résultat de repr(amenity) :", repr_output)

    # Vérifie la structure attendue
    assert isinstance(repr_output, str)
    assert repr_output.startswith("<Amenity ")
    assert amenity.id in repr_output
    assert "Jacuzzi" in repr_output


def test_str_method_of_amenity():
    """
    Vérifie que __str__() retourne une chaîne lisible au format attendu.
    """

    print(">>> Création d’un Amenity pour tester __str__()")
    amenity = Amenity("Piscine")
    str_output = str(amenity)

    print(">>> Résultat de str(amenity) :", str_output)

    # Vérifie que la chaîne retournée est correcte
    assert isinstance(str_output, str)
    assert str_output == "Commodité : Piscine"


def test_update_name_of_amenity():
    """
    Vérifie que la modification du nom met bien à jour updated_at,
    et conserve un nom valide.
    """

    amenity = Amenity("Climatisation")
    old_updated_at = amenity.updated_at

    print(">>> Avant modification :")
    print("- name =", amenity.name)
    print("- updated_at =", old_updated_at)

    # Pause pour observer un vrai changement temporel
    time.sleep(3)

    # Modification du nom
    amenity.name = "Chauffage"
    new_updated_at = amenity.updated_at

    print(">>> Après modification :")
    print("- name =", amenity.name)
    print("- updated_at =", new_updated_at)

    # Vérifications
    assert amenity.name == "Chauffage"
    assert isinstance(new_updated_at, datetime)
    assert new_updated_at > old_updated_at


def test_update_name_with_invalid_values():
    """
    Vérifie que les valeurs invalides pour name lèvent une erreur appropriée.
    """

    amenity = Amenity("Terrasse")

    # Test 1 : None → TypeError
    print(">>> Tentative avec None")
    with pytest.raises(TypeError) as exc1:
        amenity.name = None
    print(">>> Exception capturée :", exc1.value)

    # Test 2 : Chaîne vide → ValueError
    print(">>> Tentative avec chaîne vide")
    with pytest.raises(ValueError) as exc2:
        amenity.name = ""
    print(">>> Exception capturée :", exc2.value)

    # Test 3 : Chaîne d'espaces → ValueError
    print(">>> Tentative avec chaîne d'espaces")
    with pytest.raises(ValueError) as exc3:
        amenity.name = "   "
    print(">>> Exception capturée :", exc3.value)

    # Test 4 : Nom trop long → ValueError
    print(">>> Tentative avec un nom trop long (51 caractères)")
    with pytest.raises(ValueError) as exc4:
        amenity.name = "x" * 51
    print(">>> Exception capturée :", exc4.value)


def test_update_with_unknown_field():
    """
    Vérifie que l'appel de update() avec un champ inconnu
    ne modifie pas l'objet et n'ajoute pas d'attribut non autorisé.
    """

    amenity = Amenity("Télévision")
    print(">>> Avant update : name =", amenity.name)

    # Mise à jour avec une clé valide + une clé inconnue
    update_data = {
        "name": "TV HD",
        "wifi_speed": "100Mbps"  # Ce champ n'existe pas dans Amenity
    }

    amenity.update(update_data)

    print(">>> Après update : name =", amenity.name)

    # Vérifie que le champ valide a bien été mis à jour
    assert amenity.name == "TV HD"

    # Vérifie que le champ inconnu n’a pas été ajouté
    has_unknown_attr = hasattr(amenity, "wifi_speed")
    print(">>> Attribut 'wifi_speed' présent dans amenity ?", has_unknown_attr)
    assert not has_unknown_attr


def test_add_amenity_to_place():
    """
    Vérifie qu'un Amenity peut être ajouté à un Place,
    et qu'il est bien présent dans la liste des amenities.
    """

    print(">>> Création du propriétaire, du lieu et de la commodité")
    owner = User(first_name="Padmé", last_name="Naberrie", email="padme@senat.gal")

    place = Place(
        title="Appartement Naboo",
        price=120,
        owner=owner,
        description="Appartement royal avec vue sur les lacs",
        latitude=43.123,
        longitude=6.789
    )

    amenity = Amenity("Wi-Fi")

    print(">>> Ajout de l'amenity au lieu")
    place.amenities.append(amenity)

    print(">>> Contenu de place.amenities :", place.amenities)

    # Vérifie que la commodité est bien dans la liste
    assert amenity in place.amenities
    assert isinstance(place.amenities[0], Amenity)
    assert place.amenities[0].name == "Wi-Fi"


def test_add_multiple_amenities_to_place():
    """
    Vérifie que plusieurs objets Amenity peuvent être ajoutés à un Place.
    """

    print(">>> Création du propriétaire")
    owner = User(first_name="Anakin", last_name="Skywalker", email="anakin@jediorder.org")

    print(">>> Création du lieu")
    place = Place(
        title="Appartement Jedi",
        price=200,
        owner=owner,
        description="Appartement sobre avec salle d'entraînement au sabre",
        latitude=12.345,
        longitude=9.876
    )

    print(">>> Création des commodités")
    wifi = Amenity("Wi-Fi")
    parking = Amenity("Parking")
    sabre_training = Amenity("Dojo Sabre-Laser")

    print(">>> Ajout des commodités au lieu")
    place.amenities.append(wifi)
    place.amenities.append(parking)
    place.amenities.append(sabre_training)

    print(">>> Contenu final de place.amenities :")
    for amenity in place.amenities:
        print("-", amenity)

    # Vérifications
    assert len(place.amenities) == 3
    assert wifi in place.amenities
    assert parking in place.amenities
    assert sabre_training in place.amenities


def test_add_same_amenity_twice_to_place():
    """
    Vérifie le comportement si on ajoute deux fois le même Amenity à un Place.
    """

    owner = User(first_name="Obi-Wan", last_name="Kenobi", email="kenobi@jedi.org")

    place = Place(
        title="Refuge sur Tatooine",
        price=90,
        owner=owner,
        description="Abri discret dans le désert de Jundland",
        latitude=33.333,
        longitude=44.444
    )

    amenity = Amenity("Water supply")

    print(">>> Ajout deux fois de la même commodité")
    place.amenities.append(amenity)
    place.amenities.append(amenity)

    print(">>> Contenu de place.amenities :")
    for item in place.amenities:
        print("-", item)

    # On teste ici que le doublon est bien présent
    count = place.amenities.count(amenity)
    print(">>> Nombre de fois où la commodité apparaît :", count)

    assert count == 2  # Comportement par défaut d'une list Python


def test_add_non_amenity_object_to_place():
    """
    Vérifie que l'ajout d'un objet non-Amenity dans place.amenities
    est soit bloqué, soit détecté (aucun contrôle par défaut dans list).
    """

    # Propriétaire valide
    owner = User(first_name="Yoda", last_name="Unknown", email="yoda@dagobah.org")

    place = Place(
        title="Hutte sur Dagobah",
        price=50,
        owner=owner,
        description="Refuge marécageux pour la méditation",
        latitude=88.888,
        longitude=99.999
    )

    print(">>> Tentative d’ajout d’un User dans place.amenities")
    non_amenity = User(first_name="Palpatine", last_name="Sheev", email="emperor@coruscant.org")

    # Ajout d’un objet non-Amenity
    place.amenities.append(non_amenity)

    print(">>> Contenu de place.amenities :")
    for item in place.amenities:
        print("-", item)

    # Détection : au moins un élément n'est pas un Amenity
    has_non_amenity = any(not isinstance(a, Amenity) for a in place.amenities)
    print(">>> Un élément n'est pas un Amenity :", has_non_amenity)

    assert has_non_amenity is True


def test_remove_amenity_from_place():
    """
    Vérifie que l'on peut supprimer un Amenity de place.amenities
    et que la liste est correctement mise à jour.
    """

    owner = User(first_name="Bail", last_name="Organa", email="organa@alderaan.org")

    place = Place(
        title="Appartement Alderaan",
        price=180,
        owner=owner,
        description="Vue panoramique sur les montagnes d’Alderaan",
        latitude=56.789,
        longitude=12.345
    )

    wifi = Amenity("Wi-Fi")
    spa = Amenity("Spa")
    terrasse = Amenity("Terrasse")

    print(">>> Ajout de 3 commodités au lieu")
    place.amenities.extend([wifi, spa, terrasse])

    print(">>> Liste AVANT suppression :")
    for a in place.amenities:
        print("-", a)

    print(">>> Suppression de l’amenity : Spa")
    place.amenities.remove(spa)

    print(">>> Liste APRÈS suppression :")
    for a in place.amenities:
        print("-", a)

    # Vérifications
    assert spa not in place.amenities
    assert len(place.amenities) == 2
    assert wifi in place.amenities
    assert terrasse in place.amenities


def test_amenity_shared_between_places():
    """
    Vérifie qu'un même Amenity peut être associé à plusieurs Place différents.
    """

    owner1 = User(first_name="Leia", last_name="Organa", email="leia@rebellion.org")
    owner2 = User(first_name="Mon", last_name="Mothma", email="mon@senat.org")

    place1 = Place(
        title="Appartement Rebellion",
        price=150,
        owner=owner1,
        description="Centre de commandement secret",
        latitude=10.001,
        longitude=10.002
    )

    place2 = Place(
        title="Bureau du Sénat",
        price=220,
        owner=owner2,
        description="Bureau de haute sécurité sur Chandrila",
        latitude=20.001,
        longitude=20.002
    )

    shared_amenity = Amenity("HoloNet sécurisé")

    print(">>> Ajout de la même commodité dans deux lieux différents")
    place1.amenities.append(shared_amenity)
    place2.amenities.append(shared_amenity)

    print(">>> Contenu de place1.amenities :")
    for a in place1.amenities:
        print("-", a)

    print(">>> Contenu de place2.amenities :")
    for a in place2.amenities:
        print("-", a)

    # Vérifications
    assert shared_amenity in place1.amenities
    assert shared_amenity in place2.amenities
    assert place1.amenities is not place2.amenities  # deux listes indépendantes
