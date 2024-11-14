from fastapi import APIRouter, Depends, HTTPException, status

from app.db.database import DatabaseConnectionError
from app.services.segments_repository import SegmentsRepository
from app.services.segments_service import get_segments_repository

router = APIRouter()


@router.get("/segments", tags=["segments"], summary="Get all segments")
async def segments(
    segments_repository: SegmentsRepository = Depends(get_segments_repository),
):
    """Get all segments."""
    try:
        found_segments = segments_repository.get_all_segments()
        return found_segments
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}


@router.get("/segments/{location}", tags=["segments"])
async def segments_location(
    location: str,
    segments_repository: SegmentsRepository = Depends(get_segments_repository),
):
    """Get all mapped segments for a specific location."""
    try:
        area_segments = segments_repository.get_all_segments_for_area(location)
        if not area_segments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
        return area_segments

    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}
