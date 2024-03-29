from app.db.database import Database
from typing import List, Any
from datetime import datetime, timedelta
from app.utils.config import Config
from app.utils.logger import Logger
from app.models.segment_effort_data import SegmentEffortData


def map_segment_effort_data(full_segment):
    segment_id = full_segment.get("id")
    segment_name = full_segment.get("name")
    effort_count = full_segment.get("effort_count")
    fetch_date = datetime.now().strftime(Config.DATE_FORMAT)
    return SegmentEffortData(segment_id, segment_name, effort_count, fetch_date)


class SegmentsRepository:
    def __init__(self, db: Database, config: Config):
        self.config = config
        self.db = db

    def get_segment(self, segment_id: str):
        """Get segment data for a specific segment_id."""
        Logger.debug(f"Getting segment data for segment_id: {segment_id}")
        result = self.db.find_one_without_id(self.config.SEGMENTS_COLL_NAME, {"id": int(segment_id)})
        return result

    def get_cleaned_segment(self, segment_id: str):
        """Get cleaned segment data for a specific segment_id."""
        Logger.debug(f"Getting cleaned segment data for segment_id: {segment_id}")
        segment = self.get_segment(segment_id)
        if segment:
            return {
                "name": segment.get("name"),
                "id": segment.get("id"),
                "average_grade": segment.get("average_grade"),
                "start_lat": segment.get("start_latlng", [None, None])[0],
                "start_lng": segment.get("start_latlng", [None, None])[1],
                "end_lat": segment.get("end_latlng", [None, None])[0],
                "end_lng": segment.get("end_latlng", [None, None])[1],
                "local_legend": segment.get("local_legend"),
                "star_count": segment.get("star_count"),
                "effort_count": segment.get("effort_count"),
                "athlete_count": segment.get("athlete_count"),
                "kom": segment.get("xoms", {}).get("kom"),
                "map": segment.get("map"),
                "polyline": segment.get("map", {}).get("polyline"),
            }
        return None

    def get_segment_efforts(self, segment_id: str):
        """Get segment effort data for a specific segment_id."""
        Logger.debug(f"Getting segment effort data for segment_id: {segment_id}")
        result = self.db.find_one(self.config.EFFORT_COLL_NAME, {"segment_id": int(segment_id)})
        Logger.info(f"Result: {result}")
        if result:
            efforts = result.get("efforts")
            return efforts
        return None

    def get_all_segments(self) -> List[dict[str, Any]]:
        """Get all segments from the database."""
        Logger.debug("Getting all segments")
        result = self.db.find_many(self.config.SEGMENTS_COLL_NAME, {})
        return list(result)

    def get_effort_count_change_for_last_x_days(self, segment_id: str, days: int = 7) -> int | None:
        """Get the change in effort count for a segment over the last x days (default 7).
        Returns None if there is not enough data"""
        segment_data = self.get_segment_efforts(segment_id)
        if segment_data:
            x_days_ago = (datetime.now() - timedelta(days=days)).strftime(Config.DATE_FORMAT)
            efforts_last_x_days = [
                effort
                for effort in segment_data
                if datetime.strptime(effort.get("fetch_date"), Config.DATE_FORMAT) >= datetime.strptime(x_days_ago,
                                                                                                        Config.DATE_FORMAT)
            ]
            efforts_last_x_days = sorted(
                efforts_last_x_days, key=lambda x: datetime.strptime(x.get("fetch_date"), Config.DATE_FORMAT)
            )
            if len(efforts_last_x_days) >= 2:
                initial_effort_count = efforts_last_x_days[0].effort_count
                final_effort_count = efforts_last_x_days[-1].effort_count
                effort_count_change = final_effort_count - initial_effort_count
                return effort_count_change
        return None

    # TODO: the following method is not complete
    def get_effort_counts_for_date_range(self, segment_id: str, start_date: str, end_date: str) -> list[dict[
        str, Any]] | None:
        """Get the effort counts for a segment in a given date range. Returns None if there is no data.
        Returns a list of dictionaries with the fetch_date and effort_count.
        Dates should be in the format "dd-mm-yyyy"""
        segment_data = self.get_segment_efforts(segment_id)
        if segment_data:
            efforts_in_range = [
                effort
                for effort in segment_data
                if datetime.strptime(start_date, Config.DATE_FORMAT) <= datetime.strptime(effort.get("fetch_date"),
                                                                                          Config.DATE_FORMAT) <= datetime.strptime(
                    end_date, Config.DATE_FORMAT)
            ]
            return efforts_in_range
        return None
