from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)

def test_get_all_areas():
    response = client.get("/trail_areas")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert isinstance(content, list)

def test_get_single_area():
    response = client.get("/trail_areas/alghero")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    print(content)
    assert content["name"] == "Alghero"

def test_get_non_existent_area():
    response = client.get("/trail_areas/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND