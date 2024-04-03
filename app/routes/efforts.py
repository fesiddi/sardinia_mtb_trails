from fastapi import APIRouter, Request, Depends, HTTPException

from app.services.segments_repository import SegmentsRepository
from app.db.database import DatabaseConnectionError
from app.segments_data.segment_ids import segment_ids_dict
from app.services.segments_service import get_segments_repository
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="app/static/templates")



@router.get("/efforts/{location}")
async def segments_stats(request: Request, location: str, start_date: str, end_date: str,
                         segments_repository: SegmentsRepository = Depends(get_segments_repository)):
    """Get effort counts for all segments in a specific location within a date range.
    Example: /efforts/Chamonix?start_date=01-01-2024&end_date=31-01-2024"""
    segment_ids = segment_ids_dict.get(location)
    if not segment_ids:
        raise HTTPException(status_code=404, detail="Location not found")
    try:
        data = {}
        for segment_id in segment_ids.keys():
            segment = segments_repository.get_segment(segment_id)
            result = segments_repository.get_effort_counts_for_date_range(segment_id, start_date, end_date)
            if result is not None:
                data[segment_id] = {"name": segment.name, "efforts": result}
        return templates.TemplateResponse("stats.html", {"request": request, "location": location, "data": data})
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}

@router.get("/efforts/{segment_id}")
async def effort_change(segment_id: str, days: int = 7, segments_repository: SegmentsRepository = Depends(get_segments_repository)):
    """Get effort change for a specific segment over the last x days (default 7).
    Example: /efforts/33922489?days=5 or with default 7 days /efforts/33922489"""
    try:
        result = segments_repository.get_effort_count_change_for_last_x_days(segment_id, days)
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}
    if result is None:
        return {"message": "No data available for this segment"}
    return {f"effort_change_last_{days}_days": result}


@router.get("/efforts-interval/{segment_id}")
async def effort_counts(segment_id: str, start_date: str, end_date: str,
                        segments_repository: SegmentsRepository = Depends(get_segments_repository)):
    """Get effort counts for a specific segment within a date range.
    Example: /efforts/33922489?start_date=01-01-2024&end_date=31-01-2024"""
    try:
        result = segments_repository.get_effort_counts_for_date_range(segment_id, start_date, end_date)
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}
    if result is None:
        return {"message": "No data available for this segment in the given date range"}
    return {"effort_counts": result}



