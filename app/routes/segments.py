from fastapi import APIRouter, Depends, HTTPException

from app.services.segments_repository import SegmentsRepository
from app.db.database import DatabaseConnectionError
from app.segments_data.segment_ids import segment_ids_dict
from app.services.segments_service import get_segments_repository

router = APIRouter()


@router.get("/segments", tags=["segments"])
async def segments(segments_repository: SegmentsRepository = Depends(get_segments_repository)):
    """Get all segments."""
    try:
        found_segments = segments_repository.get_all_segments()
        return found_segments
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}


@router.get("/segments/{location}")
async def segments_location(location: str, segments_repository: SegmentsRepository = Depends(get_segments_repository)):
    """Get all mapped segments for a specific location."""
    segment_ids = segment_ids_dict.get(location)
    trail_area = location
    if not segment_ids:
        raise HTTPException(status_code=404, detail="Location not found")
    try:
        area_segments = segments_repository.get_all_segments_for_area(trail_area)
        return area_segments

    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}





