from typing import List, Optional, Tuple

from pydantic import BaseModel, ConfigDict


class LocalRider(BaseModel):
    name: str
    strava_id: str


class TrailBase(BaseModel):
    name: str
    coordinates: Tuple[float, float] = [0.0, 0.0]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TrailArea(BaseModel):
    name: str
    s_name: str
    description: str
    local_riders: List[LocalRider]
    instagram: List[str]
    trail_bases: Optional[List[TrailBase]] | None = None

class MessageResponse(BaseModel):
    message: str