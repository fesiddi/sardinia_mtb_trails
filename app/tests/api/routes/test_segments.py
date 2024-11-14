from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)

def test_get_all_segments():
    response = client.get("/segments")
    assert response.code == status.HTTP_200_OK

def test_segments_for_specific_location():
    response = client.get("/segments/alghero")
    assert response.status_code == status.HTTP_200_OK

def test_segment_list_for_alghero():
    response = client.get("/segments/alghero")
    assert response.status_code == status.HTTP_200_OK
    segments = response.json()
    assert segments[0]["name"] == "1. Merenderos (Red DH)"
    assert segments[1]["name"] == "2. Maranatz (Red DH)"
    assert segments[2]["name"] == "3. Timid'Huez (Black DH)"
    assert segments[3]["name"] == "4. Into the Wild (Black DH)"
    assert segments[4]["name"] == "5. Mistral (Red/Black DH)"
    assert segments[5]["name"] == "6. Easy Peasy Lemon Squeezy (Green Trail)"