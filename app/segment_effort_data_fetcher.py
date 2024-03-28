from datetime import datetime
from .logger import logger
from .segments import get_segment
from .segment_effort_data import SegmentEffortData


def fetch_segment_effort_stats(segment_id: str) -> SegmentEffortData:
    """Fetch effort stats for a segment and return a dictionary with the data."""
    logger.debug(f"Fetching stats for segment {segment_id}...")
    segment = get_segment(segment_id)
    stats = SegmentEffortData(
        id=segment.get("id"),
        name=segment.get("name"),
        effort_count=segment.get("effort_count"),
        fetch_date=datetime.now().strftime("%d-%m-%Y"),
    )
    return stats
