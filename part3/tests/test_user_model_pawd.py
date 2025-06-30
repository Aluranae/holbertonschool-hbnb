# tests/test_user_model.py

import pytest
from app.models.user import User


def test_hash_password_sets_hashed_value():
    user = User(first_name="Luke", last_name="Skywalker", email="luke@jedi.com")
    password = "Force1234!!@#"

    print(f"Avant hachage : user.password = {user.password}")  # Devrait être None ou vide

    user.hash_password(password)

    print(f"Après hachage : user.password = {user.password}")  # Devrait contenir un hash bcrypt

    assert user.password != password  # Le mot de passe ne doit pas rester en clair
    assert user.password.startswith("$2b$")  # Préfixe typique de bcrypt


def test_verify_password_success():
    print("\n Test de verify_password avec un mot de passe correct")

    # Création de l'utilisateur
    user = User(first_name="Leia", last_name="Organa", email="leia@rebellion.org")
    password = "Alderaan123!!"  # Respecte bien les règles

    # Hash du mot de passe
    user.hash_password(password)
    print(f"Hash généré : {user.password}")

    # Vérification du bon mot de passe
    result = user.verify_password(password)
    print(f"Résultat de verify_password(password) : {result}")

    assert result is True


def test_verify_password_failure():
    print("\n Test de verify_password avec un mot de passe incorrect")

    # Création de l'utilisateur
    user = User(first_name="Han", last_name="Solo", email="han@falcon.com")
    correct_password = "Millennium123!"
    wrong_password = "WrongPassword!!"

    # Hash du bon mot de passe
    user.hash_password(correct_password)
    print(f"Hash enregistré : {user.password}")

    # Vérification avec un mauvais mot de passe
    result = user.verify_password(wrong_password)
    print(f"Résultat avec mauvais mot de passe : {result}")

    assert result is False
