from datetime import datetime, timedelta
from typing import Any, List, Optional

from app.db.database import Database
from app.models.enhanced_segment import EnhancedSegment
from app.models.segment_efforts import Effort, SegmentEfforts
from app.utils.config import Config
from app.utils.logger import Logger


class SegmentsRepository:
    def __init__(self, db: Database, config: Config):
        self.config = config
        self.db = db

    def get_segment(self, segment_id: str) -> Optional[EnhancedSegment]:
        """Get segment data for a specific segment_id."""
        Logger.debug(f"Getting segment data for segment_id: {segment_id}")
        result = self.db.find_one(
            self.config.SEGMENTS_COLL_NAME, {"id": int(segment_id)}
        )
        if result:
            return EnhancedSegment(**result)
        return None

    def get_all_segments(self) -> List[EnhancedSegment]:
        """Get all segments from the database."""
        Logger.debug("Getting all segments")
        result = self.db.find_many(self.config.SEGMENTS_COLL_NAME, {})
        segments = [EnhancedSegment(**segment) for segment in result]
        return segments

    def get_all_segments_for_area(self, area: str) -> List[EnhancedSegment]:
        """Get all segments for a specific area."""
        Logger.debug(f"Getting all segments for area: {area}")
        result = self.db.find_many(
            self.config.SEGMENTS_COLL_NAME, {"trail_area": area.lower()}
        )
        segments = [EnhancedSegment(**segment) for segment in result]
        return segments

    def get_segment_efforts(self, segment_id: str) -> List[Effort] | None:
        """Get segment effort data for a specific segment_id."""
        Logger.debug(f"Getting segment effort data for segment_id: {segment_id}")
        result = self.db.find_one(
            self.config.EFFORT_COLL_NAME, {"segment_id": int(segment_id)}
        )
        efforts = SegmentEfforts.from_mongo(result).efforts
        if efforts:
            return efforts
        return None

    def get_effort_count_for_last_x_days(
        self, segment_id: str, days: int = 7
    ) -> Optional[int]:
        """Get the efforts count for a segment over the last x days (default 7).
        Returns None if there is not enough data"""
        # Fetch segment efforts
        segment_efforts = self.get_segment_efforts(segment_id)
        if not segment_efforts:
            return None

        # Filter efforts within the last x days
        recent_efforts = [
            effort
            for effort in segment_efforts
            if self._is_date_within_last_days(effort.fetch_date, days)
        ]

        # If there are less than 2 efforts, return None
        if len(recent_efforts) < 2:
            return None

        # Sort efforts by date
        recent_efforts.sort(
            key=lambda x: datetime.strptime(x.fetch_date, Config.DATE_FORMAT)
        )

        # Calculate effort count change
        initial_effort_count = recent_efforts[0].effort_count
        final_effort_count = recent_efforts[-1].effort_count
        effort_count_change = final_effort_count - initial_effort_count

        return effort_count_change

    def get_effort_counts_for_date_range(
        self, seg_id: str, start_date: str, end_date: str
    ) -> list[dict[str, Any]] | None:
        """Get the effort counts for a segment in a given date range. Returns None if there is no data.
        Returns a list of dictionaries with the fetch_date and the difference in effort_count with the previous date.
        Dates should be in the format "dd-mm-yyyy"."""
        # Fetch segment efforts
        segment_efforts = self.get_segment_efforts(seg_id)
        if segment_efforts:
            # Filter efforts within the date range and sort them by date
            efforts_in_date_range = sorted(
                (
                    effort
                    for effort in segment_efforts
                    if self._is_date_in_range(effort.fetch_date, start_date, end_date)
                ),
                key=lambda effort: datetime.strptime(
                    effort.fetch_date, Config.DATE_FORMAT
                ),
            )

            # Calculate the difference in effort count with the previous date for each effort
            effort_count_diffs = []
            for current_effort, next_effort in zip(
                efforts_in_date_range, efforts_in_date_range[1:]
            ):
                effort_count_diff = (
                    next_effort.effort_count - current_effort.effort_count
                )
                effort_count_diffs.append(
                    {
                        "fetch_date": next_effort.fetch_date,
                        "efforts": effort_count_diff,
                    }
                )

            return effort_count_diffs
        return None

    def _is_date_within_last_days(self, date: str, days: int) -> bool:
        """Check if a date is within the last x days."""
        date = datetime.strptime(date, Config.DATE_FORMAT)
        x_days_ago = datetime.now() - timedelta(days=days)
        return date >= x_days_ago

    def _is_date_in_range(self, date: str, start_date: str, end_date: str) -> bool:
        """Check if a date is within a given date range."""
        date = datetime.strptime(date, Config.DATE_FORMAT)
        start_date = datetime.strptime(start_date, Config.DATE_FORMAT)
        end_date = datetime.strptime(end_date, Config.DATE_FORMAT)
        return start_date <= date <= end_date
