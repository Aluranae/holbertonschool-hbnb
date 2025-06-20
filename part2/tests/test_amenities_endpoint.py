import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_amenity_success(client):
    data = {"name": "Wi-Fi"}
    response = client.post("/api/v1/amenities/", json=data)
    assert response.status_code == 201
    assert response.get_json()["name"] == "Wi-Fi"

def test_create_amenity_invalid(client):
    # Missing name
    response = client.post("/api/v1/amenities/", json={})
    assert response.status_code == 400

    # Name is not a string
    response = client.post("/api/v1/amenities/", json={"name": 123})
    assert response.status_code == 400

def test_list_amenities(client):
    # Create two amenities
    client.post("/api/v1/amenities/", json={"name": "Wi-Fi"})
    client.post("/api/v1/amenities/", json={"name": "Parking"})

    response = client.get("/api/v1/amenities/")
    assert response.status_code == 200
    result = response.get_json()
    assert any(a["name"] == "Wi-Fi" for a in result)
    assert any(a["name"] == "Parking" for a in result)

def test_get_single_amenity(client):
    post_resp = client.post("/api/v1/amenities/", json={"name": "Pool"})
    amenity_id = post_resp.get_json()["id"]

    get_resp = client.get(f"/api/v1/amenities/{amenity_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["name"] == "Pool"

def test_get_amenity_not_found(client):
    response = client.get("/api/v1/amenities/nonexistent")
    assert response.status_code == 404

def test_update_amenity_success(client):
    post_resp = client.post("/api/v1/amenities/", json={"name": "Old Name"})
    amenity_id = post_resp.get_json()["id"]

    put_resp = client.put(f"/api/v1/amenities/{amenity_id}", json={"name": "New Name"})
    assert put_resp.status_code == 200
    assert "updated successfully" in put_resp.get_json()["message"].lower()

def test_update_amenity_invalid(client):
    post_resp = client.post("/api/v1/amenities/", json={"name": "TV"})
    amenity_id = post_resp.get_json()["id"]

    response = client.put(f"/api/v1/amenities/{amenity_id}", json={"name": 123})
    assert response.status_code == 400

    response = client.put(f"/api/v1/amenities/{amenity_id}", json={})
    assert response.status_code == 400

def test_update_amenity_not_found(client):
    response = client.put("/api/v1/amenities/doesnotexist", json={"name": "TV"})
    assert response.status_code == 404
