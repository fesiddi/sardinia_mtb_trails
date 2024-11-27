from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, model_validator


class LatLng(BaseModel):
    lat: float
    lng: float


class Destination(BaseModel):
    href: str
    type: str
    name: str


class Xoms(BaseModel):
    kom: str
    qom: Optional[str]
    overall: str
    destination: Destination


class LocalLegend(BaseModel):
    athlete_id: int
    title: str
    profile: str
    effort_description: str
    effort_count: str
    effort_counts: Optional[Dict[str, Optional[str]]]
    destination: str


class AthleteSegmentStats(BaseModel):
    pr_elapsed_time: Optional[float]
    pr_date: Optional[str]
    pr_visibility: Optional[str]
    pr_activity_id: Optional[int]
    pr_activity_visibility: Optional[str]
    effort_count: int


class Map(BaseModel):
    id: str
    polyline: str
    resource_state: int


class RawSegment(BaseModel):
    id: int
    resource_state: int
    name: str
    activity_type: str
    distance: float
    average_grade: float
    maximum_grade: float
    elevation_high: float
    elevation_low: float
    start_latlng: LatLng
    end_latlng: LatLng
    elevation_profile: str
    climb_category: int
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    private: bool
    hazardous: bool
    starred: bool
    created_at: str
    updated_at: str
    total_elevation_gain: float
    map: Map
    effort_count: int
    athlete_count: int
    star_count: int
    athlete_segment_stats: AthleteSegmentStats
    xoms: Xoms
    local_legend: Optional[LocalLegend]

    @model_validator(mode="before")
    def convert_latlng(cls, values):
        if "start_latlng" in values and isinstance(values["start_latlng"], list):
            values["start_latlng"] = LatLng(
                lat=values["start_latlng"][0], lng=values["start_latlng"][1]
            )
        if "end_latlng" in values and isinstance(values["end_latlng"], list):
            values["end_latlng"] = LatLng(
                lat=values["end_latlng"][0], lng=values["end_latlng"][1]
            )
        return values

    @model_validator(mode="before")
    def convert_local_legend(cls, value):
        if (
            value
            and value.get("effort_counts")
            and value["effort_counts"].get("female") is None
        ):
            value["effort_counts"]["female"] = None
        return value

    model_config = ConfigDict(populate_by_name=True)
