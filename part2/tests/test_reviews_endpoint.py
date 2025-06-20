
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
    return res.get_json()["id"]

def create_amenity(client, name="Wi-Fi"):
    res = client.post("/api/v1/amenities/", json={"name": name})
    assert res.status_code == 201, f"Erreur création amenity: {res.status_code} | {res.get_json()}"
    return res.get_json()["id"]

def create_place(client, owner_id, title="Test Place"):
    amenity_id = create_amenity(client)
    data = {
        "title": title,
        "description": "Nice place",
        "price": 100.0,
        "latitude": 45.0,
        "longitude": 3.0,
        "owner_id": owner_id,
        "amenities": [amenity_id]
    }
    res = client.post("/api/v1/places/", json=data)
    assert res.status_code == 201, f"Erreur création place: {res.status_code} | {res.get_json()}"
    return res.get_json()["id"]

def create_review(client, user_id, place_id, rating=4):
    data = {
        "text": "Great place!",
        "rating": rating,
        "user_id": user_id,
        "place_id": place_id
    }
    res = client.post("/api/v1/reviews/", json=data)
    print("Review POST response:", res.status_code, res.get_json())  # utile pour debug
    return res


def test_create_review_success(client):
    user_id = create_user(client, "reviewer@example.com")
    place_id = create_place(client, user_id, "Review Place")
    res = create_review(client, user_id, place_id)
    assert res.status_code == 201
    assert res.get_json()["text"] == "Great place!"

def test_create_review_invalid_rating(client):
    user_id = create_user(client, "invalidrat@example.com")
    place_id = create_place(client, user_id, "Bad Rating Place")
    data = {
        "text": "Not good",
        "rating": 8,
        "user_id": user_id,
        "place_id": place_id
    }
    res = client.post("/api/v1/reviews/", json=data)
    assert res.status_code == 400

def test_get_reviews(client):
    user_id = create_user(client, "listrev@example.com")
    place_id = create_place(client, user_id, "List Reviews")
    create_review(client, user_id, place_id)
    res = client.get("/api/v1/reviews/")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_get_review_by_id(client):
    user_id = create_user(client, "idrev@example.com")
    place_id = create_place(client, user_id, "ID Review Place")
    res = create_review(client, user_id, place_id)
    review_id = res.get_json()["id"]
    res2 = client.get(f"/api/v1/reviews/{review_id}")
    assert res2.status_code == 200
    assert res2.get_json()["id"] == review_id

def test_update_review(client):
    user_id = create_user(client, "uprev@example.com")
    place_id = create_place(client, user_id, "Update Review Place")
    res = create_review(client, user_id, place_id)
    review_id = res.get_json()["id"]
    update = {
        "text": "Updated review text",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }
    res2 = client.put(f"/api/v1/reviews/{review_id}", json=update)
    assert res2.status_code == 200
    assert res2.get_json()["text"] == "Updated review text"

def test_delete_review(client):
    user_id = create_user(client, "delrev@example.com")
    place_id = create_place(client, user_id, "Delete Review Place")
    res = create_review(client, user_id, place_id)
    review_id = res.get_json()["id"]
    del_res = client.delete(f"/api/v1/reviews/{review_id}")
    assert del_res.status_code == 200
    get_res = client.get(f"/api/v1/reviews/{review_id}")
    assert get_res.status_code == 404

def test_get_reviews_by_place(client):
    user_id = create_user(client, "placerev@example.com")
    place_id = create_place(client, user_id, "Place With Reviews")
    create_review(client, user_id, place_id)
    res = client.get(f"/api/v1/reviews/places/{place_id}/reviews")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
