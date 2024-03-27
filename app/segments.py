import os
from typing import Any, Dict

import requests
from cachetools import TTLCache, cached
from fastapi.exceptions import HTTPException

cache = TTLCache(maxsize=1000, ttl=30000)  # 30000 / 60 to obtain minutes = 500 minutes

segment_ids_map: Dict[str, Dict[str, str]] = {
    "alghero": {
        "28448435": "Merenderos ps1",
        "28448438": "Maranatz ps2",
        "28448717": "Timid'Huez ps3",
        "28448497": "Into the wild ps4",
        "28448465": "Mistral ps5",
        "28448470": "Easy peasy ps6",
        "33922489": "Parabellum",
        "28156996": "Devallada de Tore",
        "24535220": "Okaw completo",
        "11451094": "Catorcio",
    },
    "baunei": {
        "35663742": "PS1 2024",
        "35663760": "PS2 2024",
        "35663789": "PS3 2024",
    },
    "capoterra": {
        "27667719": "Paradiso",
        "22778873": "Inferno",
        "23026998": "Purgatorio",
        "33543696": "Spaccabraccia",
        "36150152": "Scioppino",
    },
    "marci": {
        "35669866": "Bombonera",
        "33243466": "Voragini",
        "36167901": "Leggendaria",
    },
    "olbia": {
        "16432849": "DH Monte Pino",
        "14148006": "Tornanti Ps3",
        "14087488": "PS1 2018",
    },
}

strava_access_token = os.getenv("STRAVA_ACCESS_TOKEN")


@cached(cache)  # Use caching for this function
def get_segment(segment_id: str) -> Dict[str, Any]:
    global strava_access_token
    headers = {"Authorization": f"Bearer {strava_access_token}"}
    response = requests.get(
        f"https://www.strava.com/api/v3/segments/{segment_id}", headers=headers
    )
    if response.status_code == 401:
        auth_request = refresh_token()
        strava_access_token = auth_request.json().get("access_token")
        headers = {"Authorization": f"Bearer {strava_access_token}"}
        response = requests.get(
            f"https://www.strava.com/api/v3/segments/{segment_id}", headers=headers
        )
    elif response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    segment = response.json()
    cleaned_segment = clean_segment(segment)

    return cleaned_segment


def refresh_token():
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


def clean_segment(segment):
    return {
        "name": segment.get("name"),
        "id": segment.get("id"),
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


def get_segment_raw_data(segment_id: str):
    global strava_access_token
    headers = {"Authorization": f"Bearer {strava_access_token}"}
    response = requests.get(
        f"https://www.strava.com/api/v3/segments/{segment_id}", headers=headers
    )
    if response.status_code == 401:
        auth_request = refresh_token()
        strava_access_token = auth_request.json().get("access_token")
        headers = {"Authorization": f"Bearer {strava_access_token}"}
        response = requests.get(
            f"https://www.strava.com/api/v3/segments/{segment_id}", headers=headers
        )
    elif response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()
