import logging
from datetime import datetime
from typing import Any, Dict, List

from .database import Database
from .segment_ids import segment_ids_dict
from .segments import get_segment

# Set up logging
logging.basicConfig(level=logging.INFO)


def fetch_and_write_segments_stats():
    """Fetch and write effort stats for all segments in the segment_ids_dict into the database."""
    logging.info("Fetching and writing segment stats...")
    db = Database()
    for location, segments in segment_ids_dict.items():
        for segment_id in segments.keys():
            segment_stats = fetch_segment_effort_stats(segment_id)
            db.update_segment_effort_data(segment_stats)


def fetch_segment_effort_stats(segment_id: str) -> Dict[str, Any]:
    """Fetch effort stats for a segment and return a dictionary with the data."""
    logging.info(f"Fetching stats for segment {segment_id}...")
    segment = get_segment(segment_id)
    stats = {
        "id": segment.get("id"),
        "name": segment.get("name"),
        "effort_count": segment.get("effort_count"),
        "fetch_date": datetime.now().strftime("%d-%m-%Y"),
    }
    return stats


def get_effort_count_change_for_last_x_days(segment_id: str, days: int = 7) -> int | None:
    """Get the change in effort count for a segment over the last x days (default 7).
    Returns None if there is not enough data"""
    db = Database()
    segment_data = db.get_segment_effort_data(segment_id)
    if segment_data:
        x_days_ago = (datetime.now() - timedelta(days=days)).strftime("%d-%m-%Y")
        efforts_last_x_days = [
            effort
            for effort in segment_data["efforts"]
            if effort["fetch_date"] >= x_days_ago
        ]
        efforts_last_x_days = sorted(
            efforts_last_x_days, key=lambda x: x["fetch_date"]
        )
        if len(efforts_last_x_days) >= 2:
            initial_effort_count = efforts_last_x_days[0]["effort_count"]
            final_effort_count = efforts_last_x_days[-1]["effort_count"]
            effort_count_change = final_effort_count - initial_effort_count
            return effort_count_change
    return None


def get_effort_counts_for_date_range(segment_id: str, start_date: str, end_date: str) -> list[dict[str, Any]] | None:
    """Get the effort counts for a segment in a given date range. Returns None if there is no data. Returns a list of
    dictionaries with the fetch_date and effort_count. Dates should be in the format "dd-mm-yyyy"""
    db = Database()
    segment_data = db.get_segment_effort_data(segment_id)
    if segment_data:
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        efforts_in_date_range = [
            effort
            for effort in segment_data["efforts"]
            if start_date <= datetime.strptime(effort["fetch_date"], "%d-%m-%Y") <= end_date
        ]
        efforts_in_date_range = sorted(
            efforts_in_date_range, key=lambda x: x["fetch_date"]
        )
        effort_counts = [
            {
                "fetch_date": effort["fetch_date"],
                "effort_count": effort["effort_count"],
            }
            for effort in efforts_in_date_range
        ]
        return effort_counts
    return None

