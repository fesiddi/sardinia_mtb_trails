from typing import Optional

from pydantic import BaseModel

from app.models.raw_segment import LocalLegend, Map


class EnhancedSegment(BaseModel):
    id: int
    name: str
    alt_name: str
    trail_area: str
    average_grade: float
    distance: float
    difficulty: Optional[str] = ""
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
    timestamp: float

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "alt_name": self.alt_name,
            "trail_area": self.trail_area,
            "average_grade": self.average_grade,
            "distance": self.distance,
            "difficulty": self.difficulty,
            "popularity": self.popularity,
            "start_lat": self.start_lat,
            "start_lng": self.start_lng,
            "end_lat": self.end_lat,
            "end_lng": self.end_lng,
            "local_legend": self.local_legend.to_dict() if self.local_legend else None,
            "star_count": self.star_count,
            "effort_count": self.effort_count,
            "athlete_count": self.athlete_count,
            "kom": self.kom,
            "map": self.map.to_dict(),
            "polyline": self.polyline,
            "timestamp": self.timestamp,
        }
