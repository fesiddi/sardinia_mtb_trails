from pydantic import BaseModel, Field
from typing import Optional
from app.models.Segment import Segment, Map, LocalLegend


class CleanedSegment(BaseModel):
    name: str
    id: int
    average_grade: float
    start_lat: Optional[float]
    start_lng: Optional[float]
    end_lat: Optional[float]
    end_lng: Optional[float]
    local_legend: Optional[LocalLegend]
    star_count: int
    effort_count: int
    athlete_count: int
    kom: Optional[str]
    map: Map
    polyline: Optional[str]

    @classmethod
    def from_segment(cls, segment: Segment):
        return cls(
            name=segment.name,
            id=segment.id,
            average_grade=segment.average_grade,
            start_lat=segment.start_latlng.lat,
            start_lng=segment.start_latlng.lng,
            end_lat=segment.end_latlng.lat,
            end_lng=segment.end_latlng.lng,
            local_legend=segment.local_legend,
            star_count=segment.star_count,
            effort_count=segment.effort_count,
            athlete_count=segment.athlete_count,
            kom=segment.xoms.kom,
            map=segment.map,
            polyline=segment.map.polyline,
        )
