import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user_success(client):
    user_data = {
        "first_name": "Alice",
        "last_name": "Doe",
        "email": "alice@example.com"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    assert response.json["first_name"] == "Alice"
    assert response.json["email"] == "alice@example.com"

def test_create_user_duplicate_email(client):
    user_data = {
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob@example.com"
    }
    # Première création
    response1 = client.post("/api/v1/users/", json=user_data)
    assert response1.status_code == 201
    # Deuxième création avec le même email
    response2 = client.post("/api/v1/users/", json=user_data)
    assert response2.status_code == 400
    assert "email" in response2.get_json().get("message", "").lower()

def test_create_user_invalid_data(client):
    # Données manquantes
    user_data = {
        "first_name": "Charlie"
        # last_name et email manquants
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400

def test_get_users(client):
    # Ajoute un utilisateur
    user_data = {
        "first_name": "Diana",
        "last_name": "Prince",
        "email": "diana@example.com"
    }
    client.post("/api/v1/users/", json=user_data)
    # Récupère la liste
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    users = response.get_json()
    assert isinstance(users, list)
    assert any(u["email"] == "diana@example.com" for u in users)

def test_update_user_success(client):
    # Crée un utilisateur
    user_data = {
        "first_name": "Eve",
        "last_name": "Adams",
        "email": "eve@example.com"
    }
    post_resp = client.post("/api/v1/users/", json=user_data)
    user_id = post_resp.get_json().get("id")
    # Modifie l'utilisateur
    update_data = {
        "first_name": "Evelyn",
        "last_name": "Adams",
        "email": "eve@example.com"
    }
    put_resp = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert put_resp.status_code == 200
    assert put_resp.get_json()["first_name"] == "Evelyn"

def test_update_user_not_found(client):
    # Tente de modifier un utilisateur inexistant
    update_data = {
        "first_name": "Ghost",
        "last_name": "User",
        "email": "ghost@example.com"
    }
    put_resp = client.put("/api/v1/users/doesnotexist", json=update_data)
    assert put_resp.status_code == 404

def test_update_user_duplicate_email(client):
    # user1
    user1 = {
        "first_name": "Tom",
        "last_name": "Hanks",
        "email": "tom@example.com"
    }
    user2 = {
        "first_name": "Jerry",
        "last_name": "Mouse",
        "email": "jerry@example.com"
    }

    client.post("/api/v1/users/", json=user1)
    post2 = client.post("/api/v1/users/", json=user2)
    user2_id = post2.get_json()["id"]

    # Essaye de mettre user2 avec l’email de user1
    updated = {
        "first_name": "Jerry",
        "last_name": "Mouse",
        "email": "tom@example.com",  # email de user1
    }

    response = client.put(f"/api/v1/users/{user2_id}", json=updated)
    assert response.status_code == 400
