from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)

def test_get_efforts_for_specific_location():
    response = client.get("/efforts/alghero?start_date=01-10-2024&end_date=31-10-2024")
    assert response.status_code == status.HTTP_200_OK