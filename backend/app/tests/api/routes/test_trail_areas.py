from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_all_areas():
    response = client.get("/api/trail-areas")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert isinstance(content, list)


def test_get_single_area():
    response = client.get("/api/trail-areas/alghero")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    print(content)
    assert content["name"] == "Alghero"


def test_get_non_existent_area():
    response = client.get("/api/trail-areas/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
