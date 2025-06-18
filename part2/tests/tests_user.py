"""tests/test_user.py

Teste la création de l'entité User (valeurs valides uniquement).
"""

import pytest
import time
from app.models.user import User
from app.models.place import Place


def test_create_valid_user():
    """
    Vérifie qu'un User valide peut être créé sans erreur,
    et que ses attributs sont correctement initialisés.
    """
    user = User(first_name="Leia", last_name="Organa", email="leia@rebellion.org",)

    print(f"[DEBUG] Created user → {user}")
    print(f"[INFO] Email = {user.email}")
    print(f"[INFO] ID = {user.id}")
    print(f"[INFO] created_at = {user.created_at}")

    assert isinstance(user, User)
    assert user.first_name == "Leia"
    assert user.last_name == "Organa"
    assert user.email == "leia@rebellion.org"
    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None


def test_update_user_attribute():
    """
    Vérifie que la modification d'un attribut met à jour updated_at.
    """
    user = User(first_name="Han", last_name="Solo", email="han@falcon.com",)
    original_updated_at = user.updated_at

    # Pause pour observer une vraie différence temporelle
    time.sleep(3)

    # Modification d'un attribut
    user.first_name = "Han-Leader"
    user.save()  # méthode héritée de Base, met à jour updated_at

    print(f"[DEBUG] Updated user → {user}")
    print(f"[INFO] updated_at (after update) = {user.updated_at}")

    assert user.first_name == "Han-Leader"
    assert user.updated_at > original_updated_at


def test_user_update_method_on_valid_attribute():
    """
    Vérifie que la méthode update() modifie un attribut existant.
    """
    user = User(first_name="Padmé", last_name="Naberrie", email="padme@senate.org",)
    old_updated_at = user.updated_at

    time.sleep(1)
    user.update({"last_name": "Amidala"})

    assert user.last_name == "Amidala"
    assert user.updated_at > old_updated_at


def test_user_update_method_ignores_unknown_attribute():
    """
    Vérifie que la méthode update() ignore les clés inconnues du dictionnaire.
    """
    user = User(first_name="Anakin", last_name="Skywalker", email="anakin@jedi.org",)
    user.update({"rank": "Knight"})

    assert not hasattr(user, "rank")


def test_user_update_multiple_fields():
    """
    Vérifie la mise à jour simultanée de plusieurs champs.
    """
    user = User(first_name="Ben", last_name="Kenobi", email="ben@jedi.org",)

    user.update({
        "first_name": "Obi-Wan",
        "email": "obiwan@jedi.org"
    })

    assert user.first_name == "Obi-Wan"
    assert user.email == "obiwan@jedi.org"


def test_user_creation_missing_fields():
    """
    Vérifie qu'une exception est levée si des champs requis sont manquants.
    """
    with pytest.raises(TypeError) as exc_info:
        User(first_name="Luke")  # manque last_name et email

    print(f"[INFO] Exception levée → {exc_info.value}")
    assert "last_name" in str(exc_info.value) or "email" in str(exc_info.value)


def test_user_creation_empty_fields():
    """
    Vérifie qu'une exception est levée si les champs requis sont vides ou None.
    """
    # Cas 1 : email vide
    with pytest.raises(ValueError) as exc_email:
        User(first_name="Padmé", last_name="Naberrie", email="",)

    print(f"[INFO] Email vide → {exc_email.value}")
    assert "email" in str(exc_email.value).lower()

    # Cas 2 : prénom vide
    with pytest.raises(ValueError) as exc_first:
        User(first_name="", last_name="Skywalker", email="anakin@jedi.org")

    print(f"[INFO] Prénom vide → {exc_first.value}")
    assert "required" in str(exc_first.value).lower()

    # Cas 3 : nom vide
    with pytest.raises(ValueError) as exc_last:
        User(first_name="Anakin", last_name="", email="anakin@jedi.org")

    print(f"[INFO] Nom vide → {exc_last.value}")
    assert "required" in str(exc_last.value).lower()


def test_user_creation_invalid_types():
    """
    Vérifie que des types incorrects provoquent une exception.
    """
    # Cas 1 : prénom en int
    with pytest.raises(TypeError) as exc_type1:
        User(first_name=42, last_name="Kenobi", email="obiwan@jedi.org")

    print(f"[INFO] Type prénom invalide → {exc_type1.value}")
    assert "first name must be a string" in str(exc_type1.value).lower()

    # Cas 2 : email en list
    with pytest.raises(TypeError) as exc_type2:
        User(first_name="Obi-Wan", last_name="Kenobi", email=["kenobi@jedi.org"])

    print(f"[INFO] Type email invalide → {exc_type2.value}")
    assert "email" in str(exc_type2.value).lower()


def test_user_creation_invalid_email_format():
    """
    Vérifie que des emails au format invalide sont rejetés.
    """
    # Pas d’arobase
    with pytest.raises(ValueError) as exc1:
        User(first_name="Qui-Gon", last_name="Jinn", email="quigon.jedi.org",)

    print(f"[INFO] Email sans @ → {exc1.value}")
    assert "email" in str(exc1.value).lower()

    # Double @
    with pytest.raises(ValueError) as exc2:
        User(first_name="Count", last_name="Dooku", email="dooku@@sith.org",)

    print(f"[INFO] Email avec @@ → {exc2.value}")
    assert "email" in str(exc2.value).lower()

    # Pas de domaine
    with pytest.raises(ValueError) as exc3:
        User(first_name="General", last_name="Grievous", email="grievous@",)

    print(f"[INFO] Email sans domaine → {exc3.value}")
    assert "email" in str(exc3.value).lower()


def test_user_creation_invalid_email_double_at():
    """
    Vérifie que l'email avec double arobase est rejeté.
    """
    with pytest.raises(ValueError) as exc:
        User(first_name="Count", last_name="Dooku", email="dooku@@sith.org",)

    print(f"[INFO] Email avec @@ → {exc.value}")
    assert "email" in str(exc.value).lower()


def test_user_update_with_unknown_attribute():
    """
    Vérifie qu'une tentative d'ajout d'un champ inconnu sur un User échoue.
    """
    user = User(first_name="Bail", last_name="Organa", email="bail@alderaan.org",)

    try:
        user.rank = "senator"  # champ non défini dans la classe User
        print(f"[DEBUG] Unexpected attribute rank → {user.rank}")
        assert not hasattr(user, "rank"), "User should not accept unknown attributes"
    except AttributeError:
        print("[INFO] AttributeError correctly raised")
        assert True


def test_user_id_and_created_at_immutability():
    """
    Vérifie que id et created_at ne peuvent plus être modifiés (grâce à @property).
    """
    user = User(first_name="Cassian", last_name="Andor", email="cassian@rebellion.org")

    with pytest.raises(AttributeError, match="id is immutable"):
        user.id = "FAKE-ID"

    with pytest.raises(AttributeError, match="created_at is immutable"):
        user.created_at = "3019-01-01 00:00:00"


def test_user_str():
    """
    Vérifie que la représentation en chaîne (__str__) est correcte.
    """
    user = User(first_name="Lando", last_name="Calrissian", email="lando@cloudcity.org")
    expected = "Lando Calrissian (lando@cloudcity.org)"
    assert str(user) == expected


def test_user_email_case_insensitive():
    """
    Vérifie que l'email est stocké en minuscules, même si saisi en majuscules.
    """
    user = User(first_name="Rex", last_name="CT-7567", email="REX@REPUBLIC.ORG")
    assert user.email == "rex@republic.org"


def test_user_update_does_not_add_invalid_keys():
    """
    Vérifie que .update() ignore les clés inconnues sans lever d'erreur.
    """
    user = User(first_name="Sabine", last_name="Wren", email="sabine@mandalore.org")
    user.update({"faction": "Rebels"})  # attribut inconnu
    assert not hasattr(user, "faction")


def test_user_repr_contains_id_and_email():
    """
    Vérifie que __repr__ contient l'id et l'email (pour le debug).
    """
    user = User(first_name="Bo", last_name="Katan", email="bo@mandalore.org")
    result = repr(user)
    assert user.id in result
    assert user.email in result


def test_user_equality_reference():
    """
    Vérifie qu'un user n'est égal qu'à lui-même (par défaut en Python).
    """
    user1 = User(first_name="Hera", last_name="Syndulla", email="hera@ghost.org")
    user2 = user1
    user3 = User(first_name="Hera", last_name="Syndulla", email="hera@ghost.org")
    assert user1 == user2
    assert user1 is not user3
    assert user1 != user3


def test_user_equality_same_id():
    """
    Vérifie que deux instances de User avec le même id sont considérées égales.
    """
    user1 = User(first_name="Jyn", last_name="Erso", email="jyn@rogueone.org")
    user2 = User(first_name="Cassian", last_name="Andor", email="cassian@rebellion.org")

    # Forcer le même id
    object.__setattr__(user2, "_id", user1.id)

    print(f"[DEBUG] user1.id = {user1.id}")
    print(f"[DEBUG] user2.id = {user2.id}")

    assert user1 == user2
    assert user1 is not user2


def test_user_place_relationship():
    """
    Vérifie que l'on peut associer plusieurs Place à un User.
    """
    user = User(first_name="Padmé", last_name="Naberrie", email="padme@senate.repub")

    place1 = Place(
        title="Appartement de Naboo",
        description="Résidence royale avec vue sur le lac",
        price=250,
        latitude=44.5,
        longitude=6.2,
        owner=user
    )

    place2 = Place(
        title="Refuge de Varykino",
        description="Maison de vacances familiale dans les montagnes de Naboo",
        price=300,
        latitude=45.0,
        longitude=6.5,
        owner=user
    )

    assert place1.owner == user
    assert place2.owner == user

    user.places.append(place1)
    user.places.append(place2)

    assert len(user.places) == 2
    assert place1 in user.places
    assert place2 in user.places
