import os
from typing import Any, Dict
import requests
from fastapi.exceptions import HTTPException


class StravaApi:
    def __init__(self):
        self.strava_access_token = os.getenv("STRAVA_ACCESS_TOKEN")

    def get_segment(self, segment_id: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.strava_access_token}"}
        response = requests.get(
            f"https://www.strava.com/api/v3/segments/{segment_id}", headers=headers
        )
        if response.status_code == 401:
            auth_request = self.refresh_token()
            self.strava_access_token = auth_request.json().get("access_token")
            headers = {"Authorization": f"Bearer {self.strava_access_token}"}
            response = requests.get(
                f"https://www.strava.com/api/v3/segments/{segment_id}", headers=headers
            )
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        segment = response.json()
        cleaned_segment = self.clean_segment(segment)

        return cleaned_segment

    def get_segment_raw_data(self, segment_id: str):
        headers = {"Authorization": f"Bearer {self.strava_access_token}"}
        response = requests.get(
            f"https://www.strava.com/api/v3/segments/{segment_id}", headers=headers
        )
        if response.status_code == 401:
            auth_request = self.refresh_token()
            self.strava_access_token = auth_request.json().get("access_token")
            headers = {"Authorization": f"Bearer {self.strava_access_token}"}
            response = requests.get(
                f"https://www.strava.com/api/v3/segments/{segment_id}", headers=headers
            )
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

    def clean_segment(self, segment):
        return {
            "name": segment.get("name"),
            "id": segment.get("id"),
            "average_grade": segment.get("average_grade"),
            "start_lat": segment.get("start_latlng", [None, None])[0],
            "start_lng": segment.get("start_latlng", [None, None])[1],
            "end_lat": segment.get("end_latlng", [None, None])[0],
            "end_lng": segment.get("end_latlng", [None, None])[1],
            "local_legend": segment.get("local_legend"),
            "star_count": segment.get("star_count"),
            "effort_count": segment.get("effort_count"),
            "athlete_count": segment.get("athlete_count"),
            "kom": segment.get("xoms", {}).get("kom"),
            "map": segment.get("map"),
            "polyline": segment.get("map", {}).get("polyline"),
        }

    def refresh_token(self):
        auth_request = requests.post(
            f"https://www.strava.com/api/v3/oauth/token",
            data={
                "client_id": os.getenv("STRAVA_CLIENT_ID"),
                "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
                "grant_type": "refresh_token",
                "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
            },
        )
        if auth_request.status_code != 200:
            raise HTTPException(
                status_code=auth_request.status_code, detail=auth_request.json()
            )
        return auth_request
