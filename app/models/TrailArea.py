from typing import List, Optional, Tuple
from pydantic import BaseModel


class LocalRider(BaseModel):
    name: str
    strava_id: str


class TrailBase(BaseModel):
    name: str
    coordinates: Tuple[float, float] = [0.0, 0.0]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Base1",
                "coordinates": [12.34, 56.78]
            }
        }


class TrailArea(BaseModel):
    name: str
    s_name: str
    description: str
    local_riders: List[LocalRider]
    instagram: List[str]
    trail_bases: Optional[List[TrailBase]] | None = None
