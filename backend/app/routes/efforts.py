from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.db.database import DatabaseConnectionError
from app.services.segments_repository import SegmentsRepository
from app.services.segments_service import get_segments_repository

router = APIRouter()

templates = Jinja2Templates(directory="app/static/templates")


class EffortsDaysResponse(BaseModel):
    efforts: int


class EffortEntry(BaseModel):
    fetch_date: str
    efforts: int


EffortsCountResponse = List[EffortEntry]


@router.get("/efforts/{location}")
async def segments_stats(
    request: Request,
    location: str,
    start_date: str,
    end_date: str,
    segments_repository: SegmentsRepository = Depends(get_segments_repository),
):
    """Get efforts count for all segments in a specific location within a date range.
    Example: /api/efforts/alghero?start_date=01-10-2024&end_date=31-10-2024"""
    segments = segments_repository.get_all_segments_for_area(location)
    if not segments:
        raise HTTPException(status_code=404, detail="Location not found")
    try:
        data = {}
        for segment in segments:
            result = segments_repository.get_effort_counts_for_date_range(
                str(segment.id), start_date, end_date
            )
            if result is not None:
                data[segment.id] = {
                    "name": segment.alt_name,
                    "id": segment.id,
                    "efforts": result,
                }
        return templates.TemplateResponse(
            request, "stats.html", {"location": location, "data": data}
        )
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}


@router.get("/efforts-days/{segment_id}", response_model=EffortsDaysResponse)
async def effort_last_days(
    segment_id: str,
    days: int = 7,
    segments_repository: SegmentsRepository = Depends(get_segments_repository),
):
    """Get efforts count for a specific segment over the last x days (default 7).
    Example: /api/efforts-days/33922489?days=5 or with default 7 days /efforts/33922489
    """
    try:
        result = segments_repository.get_effort_count_for_last_x_days(segment_id, days)
        if result is None:
            return {"message": "No data available for this segment"}
        return {"efforts": result}
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}


@router.get("/efforts-interval/{segment_id}", response_model=EffortsCountResponse)
async def effort_counts(
    segment_id: str,
    start_date: str,
    end_date: str,
    segments_repository: SegmentsRepository = Depends(get_segments_repository),
):
    """Get efforts count for a specific segment within a date range.
    Example: /api/efforts-interval/33922489?start_date=01-10-2024&end_date=30-10-2024"""
    try:
        result = segments_repository.get_effort_counts_for_date_range(
            segment_id, start_date, end_date
        )
        if result is None:
            return {
                "message": "No data available for this segment in the given date range"
            }
        return result
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}
    except ValueError as e:
        return {"message": f"Invalid date format: {e}"}
    except Exception as e:
        return {"message": f"Error fetching segment stats: {e}"}
