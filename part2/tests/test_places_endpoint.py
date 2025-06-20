
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def create_user(client, email="user@example.com"):
    data = {
        "first_name": "User",
        "last_name": "Test",
        "email": email
    }
    res = client.post("/api/v1/users/", json=data)
    assert res.status_code == 201, f"Erreur création user: {res.status_code} | {res.get_json()}"
    return res.get_json()

def create_amenity(client, name="Wi-Fi"):
    res = client.post("/api/v1/amenities/", json={"name": name})
    assert res.status_code == 201, f"Erreur création amenity: {res.status_code} | {res.get_json()}"
    return res.get_json()

def create_place(client, owner_id, title="Test Place"):
    amenity = create_amenity(client)
    data = {
        "title": title,
        "description": "Nice place",
        "price": 100.0,
        "latitude": 45.0,
        "longitude": 3.0,
        "owner_id": owner_id,
        "amenities": [amenity["id"]]
    }
    res = client.post("/api/v1/places/", json=data)
    assert res.status_code == 201, f"Erreur création place: {res.status_code} | {res.get_json()}"
    return res.get_json()

def test_update_place_success(client):
    user = create_user(client, email="user5@example.com")
    amenity = create_amenity(client)
    place = create_place(client, user["id"], title="ToUpdate")
    update = {
        "title": "Updated Title",
        "description": "Changed",
        "price": 110,
        "latitude": 35.0,
        "longitude": 45.0,
        "owner_id": user["id"],
        "amenities": [amenity["id"]],
        "reviews": []
    }
    res = client.put(f"/api/v1/places/{place['id']}", json=update)
    assert res.status_code == 200
    assert res.get_json()["title"] == "Updated Title"

def test_update_place_invalid_amenity(client):
    user = create_user(client, email="user6@example.com")
    place = create_place(client, user["id"], title="BadAmenity")
    update = {
        "title": "BadAmenity",
        "description": "Test",
        "price": 70,
        "latitude": 10,
        "longitude": 10,
        "owner_id": user["id"],
        "amenities": ["invalid_amenity_id"],
        "reviews": []
    }
    res = client.put(f"/api/v1/places/{place['id']}", json=update)
    assert res.status_code == 400
    assert "Amenity with id" in res.get_json()["error"]

def test_create_place_success(client):
    user = create_user(client, "createplace@example.com")
    place = create_place(client, user["id"], title="Beautiful Home")
    assert place["title"] == "Beautiful Home"
    assert place["owner_id"] == user["id"]

def test_get_place_by_id(client):
    user = create_user(client, "getplace@example.com")
    created_place = create_place(client, user["id"], title="Specific Place")
    res = client.get(f"/api/v1/places/{created_place['id']}")
    assert res.status_code == 200
    assert res.get_json()["id"] == created_place["id"]

def test_create_place_missing_field(client):
    user = create_user(client, "missingfield@example.com")
    data = {
        "description": "No title",
        "price": 50.0,
        "latitude": 0.0,
        "longitude": 0.0,
        "owner_id": user["id"],
        "amenities": []
    }
    res = client.post("/api/v1/places/", json=data)
    res_json = res.get_json()
    assert res.status_code == 400
    assert "title" in res_json.get("error", "")
