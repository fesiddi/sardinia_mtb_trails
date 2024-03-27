import logging
from datetime import datetime
from typing import Any, Dict

from .database import Database
from .google_sheets import (authorize_and_open_sheet, format_data_for_sheet,
                            update_google_sheet)
from .segments import get_segment, segment_ids_map

# Set up logging
logging.basicConfig(level=logging.INFO)


def fetch_and_write_segments_stats():
    logging.info("Fetching and writing segment stats...")
    result = []
    for location, segments in segment_ids_map.items():
        for segment_id in segments.keys():
            segment_stats = get_segment_effort_stats(segment_id)
            result.append(segment_stats)

    db = Database()
    db.write_to_mongodb(result)

    client, sheet = authorize_and_open_sheet()
    if not sheet:
        return

    formatted_data = format_data_for_sheet(result)
    update_google_sheet(sheet, formatted_data)


def get_segment_effort_stats(segment_id: str) -> Dict[str, Any]:
    logging.info(f"Getting stats for segment {segment_id}...")
    segment = get_segment(segment_id)
    stats = {
        "id": segment.get("id"),
        "name": segment.get("name"),
        "effort_count": segment.get("effort_count"),
        "fetch_date": datetime.now().strftime("%d-%m-%Y"),
    }
    return stats
