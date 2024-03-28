from .database import Database
from .segment_effort_data import SegmentEffortData
from typing import List


class SegmentStatsDAO:
    def __init__(self, db: Database):
        self.db = db

    def update_segment_effort_data(self, segment: SegmentEffortData):
        self.db.update_segment_effort_data(segment)

    def get_segment_effort_data(self, segment_id: str) -> List[SegmentEffortData] | None:
        raw_data = self.db.get_segment_effort_data(segment_id)
        if raw_data:
            segment_effort_data = [
                SegmentEffortData(
                    id=effort["id"],
                    name=effort["name"],
                    effort_count=effort["effort_count"],
                    fetch_date=effort["fetch_date"],
                )
                for effort in raw_data["efforts"]
            ]
            return segment_effort_data
        return None
