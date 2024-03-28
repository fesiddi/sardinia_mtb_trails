from dataclasses import dataclass


@dataclass
class SegmentEffortData:
    id: str
    name: str
    effort_count: int
    fetch_date: str
