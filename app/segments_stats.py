from datetime import datetime, timedelta
from typing import Any

from .segment_ids import segment_ids_dict
from .segment_effort_data_fetcher import fetch_segment_effort_stats
from .segment_stats_dao import SegmentStatsDAO
from .logger import logger


def fetch_and_write_segments_stats(dao: SegmentStatsDAO):
    """Fetch and write effort stats for all segments in the segment_ids_dict into the database."""
    logger.debug("Fetching and writing segment stats...")
    for location, segments in segment_ids_dict.items():
        for segment_id in segments.keys():
            segment_stats = fetch_segment_effort_stats(segment_id)
            dao.update_segment_effort_data(segment_stats)


def get_effort_count_change_for_last_x_days(dao: SegmentStatsDAO, segment_id: str, days: int = 7) -> int | None:
    """Get the change in effort count for a segment over the last x days (default 7).
    Returns None if there is not enough data"""
    segment_data = dao.get_segment_effort_data(segment_id)
    if segment_data:
        x_days_ago = (datetime.now() - timedelta(days=days)).strftime("%d-%m-%Y")
        efforts_last_x_days = [
            effort
            for effort in segment_data
            if datetime.strptime(effort.fetch_date, "%d-%m-%Y") >= datetime.strptime(x_days_ago, "%d-%m-%Y")
        ]
        efforts_last_x_days = sorted(
            efforts_last_x_days, key=lambda x: datetime.strptime(x.fetch_date, "%d-%m-%Y")
        )
        if len(efforts_last_x_days) >= 2:
            initial_effort_count = efforts_last_x_days[0].effort_count
            final_effort_count = efforts_last_x_days[-1].effort_count
            effort_count_change = final_effort_count - initial_effort_count
            return effort_count_change
    return None


def get_effort_counts_for_date_range(dao: SegmentStatsDAO, segment_id: str, start_date: str, end_date: str) -> list[dict[str, Any]] | None:
    """Get the effort counts for a segment in a given date range. Returns None if there is no data. Returns a list of
    dictionaries with the fetch_date and effort_count. Dates should be in the format "dd-mm-yyyy"""
    segment_data = dao.get_segment_effort_data(segment_id)
    if segment_data:
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        efforts_in_date_range = [
            effort
            for effort in segment_data
            if start_date <= datetime.strptime(effort.fetch_date, "%d-%m-%Y") <= end_date
        ]
        efforts_in_date_range = sorted(
            efforts_in_date_range, key=lambda x: x["fetch_date"]
        )
        effort_counts = [
            {
                "fetch_date": effort.fetch_date,
                "effort_count": effort.effort_count,
            }
            for effort in efforts_in_date_range
        ]
        return effort_counts
    return None
