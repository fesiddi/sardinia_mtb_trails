from pydantic import BaseModel
from typing import Optional
from app.models.RawSegment import RawSegment, Map, LocalLegend


class EnhancedSegment(BaseModel):
    name: str
    alt_name: str
    id: int
    trail_area: str
    average_grade: float
    difficulty: Optional[str] = ''
    popularity: Optional[int] = 0
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
    def from_segment(cls, segment: RawSegment, trail_area: str):
        return cls(
            name=segment.name,
            alt_name=segment.name,
            id=segment.id,
            trail_area=trail_area,
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
