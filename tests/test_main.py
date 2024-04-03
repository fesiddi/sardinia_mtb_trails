from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_segments_location_for_capoterra():
    response = client.get("/segments/capoterra")
    assert response.status_code == 200


def test_segment_list_for_alghero():
    response = client.get("/segments/alghero")
    assert response.status_code == 200
    segments = response.json()
    assert len(segments) == 10
    assert segments[0]["name"] == "1. Merenderos (Red DH)"
    assert segments[1]["name"] == "2. Maranatz (Red DH)"
    assert segments[2]["name"] == "3. Timid'Huez (Black DH)"
    assert segments[3]["name"] == "4. Into the Wild (Black DH)"
    assert segments[4]["name"] == "5. Mistral (Red/Black DH)"
    assert segments[5]["name"] == "6. Easy Peasy Lemon Squeezy (Green Trail)"
