import json
import pytest
from app import create_app
from app.services.facade import HBnBFacade

@pytest.fixture
def client():
    app = create_app()  # ta fonction pour créer l'app Flask
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_amenity(client):
    data = {"name": "Wi-Fi"}
    response = client.post('/api/v1/amenities/', 
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 201
    resp_json = response.get_json()
    assert 'id' in resp_json
    assert resp_json['name'] == "Wi-Fi"

def test_get_all_amenities(client):
    # Crée une amenity d'abord
    client.post('/api/v1/amenities/', 
                data=json.dumps({"name": "Pool"}),
                content_type='application/json')

    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200
    resp_json = response.get_json()
    assert isinstance(resp_json, list)
    assert any(amenity['name'] == 'Pool' for amenity in resp_json)

def test_get_amenity_by_id(client):
    # Crée une amenity
    response = client.post('/api/v1/amenities/', 
                           data=json.dumps({"name": "Gym"}),
                           content_type='application/json')
    amenity_id = response.get_json()['id']

    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    resp_json = response.get_json()
    assert resp_json['id'] == amenity_id
    assert resp_json['name'] == 'Gym'

def test_get_amenity_not_found(client):
    response = client.get('/api/v1/amenities/nonexistent-id')
    assert response.status_code == 404

def test_update_amenity(client):
    # Crée une amenity
    response = client.post('/api/v1/amenities/', 
                           data=json.dumps({"name": "Spa"}),
                           content_type='application/json')
    amenity_id = response.get_json()['id']

    # Mise à jour
    updated_data = {"name": "Updated Spa"}
    response = client.put(f'/api/v1/amenities/{amenity_id}', 
                          data=json.dumps(updated_data),
                          content_type='application/json')
    assert response.status_code == 200
    resp_json = response.get_json()
    assert resp_json['message'] == "Amenity updated successfully"

    # Vérifie la mise à jour
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.get_json()['name'] == "Updated Spa"

def test_update_amenity_not_found(client):
    updated_data = {"name": "Nonexistent"}
    response = client.put('/api/v1/amenities/nonexistent-id', 
                          data=json.dumps(updated_data),
                          content_type='application/json')
    assert response.status_code == 404

def test_create_amenity_invalid_data(client):
    # Envoie un body vide
    response = client.post('/api/v1/amenities/', 
                           data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 400
