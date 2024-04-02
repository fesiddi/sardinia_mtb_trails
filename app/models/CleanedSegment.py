from pydantic import BaseModel, Field
from typing import Optional
from app.models.Segment import Segment


class CleanedSegment(BaseModel):
    name: str
    id: int
    average_grade: float
    start_lat: Optional[float]
    start_lng: Optional[float]
    end_lat: Optional[float]
    end_lng: Optional[float]
    local_legend: Optional[dict]
    star_count: int
    effort_count: int
    athlete_count: int
    kom: Optional[str]
    map: dict
    polyline: Optional[str]

    @classmethod
    def from_segment(cls, segment: Segment):
        return cls(
            name=segment.get("name"),
            id=segment.get("id"),
            average_grade=segment.get("average_grade"),
            start_lat=segment.get("start_latlng", [None, None])[0],
            start_lng=segment.get("start_latlng", [None, None])[1],
            end_lat=segment.get("end_latlng", [None, None])[0],
            end_lng=segment.get("end_latlng", [None, None])[1],
            local_legend=segment.get("local_legend"),
            star_count=segment.get("star_count"),
            effort_count=segment.get("effort_count"),
            athlete_count=segment.get("athlete_count"),
            kom=segment.get("xoms", {}).get("kom"),
            map=segment.get("map"),
            polyline=segment.get("map", {}).get("polyline"),
        )
