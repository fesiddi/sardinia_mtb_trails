from typing import List
from pydantic import BaseModel


class LocalRider(BaseModel):
    name: str
    strava_id: str


class TrailArea(BaseModel):
    name: str
    s_name: str
    description: str
    local_riders: List[LocalRider]
    instagram: List[str]
