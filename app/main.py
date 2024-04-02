import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.segments_data.segment_ids import segment_ids_dict
from app.services.segments_repository import SegmentsRepository
from app.segments_data.trail_areas_data import trail_areas_data
from app.db.database import Database, DatabaseConnectionError
from app.utils.config import Config

load_dotenv()

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)
templates = Jinja2Templates(directory="app/static/templates")

config = Config()


@app.get("/")
async def home_route(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "trail_areas_data": trail_areas_data}
    )


@app.get("/segments")
async def segments():
    """Get all segments."""
    try:
        db = Database(config)
        segments_repository = SegmentsRepository(db, config)
        found_segments = segments_repository.get_all_segments()
        return found_segments
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}


@app.get("/location/{location}")
async def segments_location(location):
    """Get all mapped segments for a specific location."""
    segment_ids = segment_ids_dict.get(location)
    if not segment_ids:
        raise HTTPException(status_code=404, detail="Location not found")
    try:
        db = Database(config)
        segments_repository = SegmentsRepository(db, config)
        segments = [segments_repository.get_cleaned_segment(segment_id) for segment_id in segment_ids.keys()]
        return segments

    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}


@app.get("/effort_change/{segment_id}")
async def effort_change(segment_id: str, days: int = 7):
    """Get effort change for a specific segment over the last x days (default 7)."""
    try:
        db = Database(config)
        segments_repository = SegmentsRepository(db, config)
        result = segments_repository.get_effort_count_change_for_last_x_days(segment_id, days)
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}
    if result is None:
        return {"message": "No data available for this segment"}
    return {f"effort_change_last_{days}_days": result}


@app.get("/effort_counts/{segment_id}")
async def effort_counts(segment_id: str, start_date: str, end_date: str):
    """Get effort counts for a specific segment within a date range."""
    try:
        db = Database(config)
        segments_repository = SegmentsRepository(db, config)
        result = segments_repository.get_effort_counts_for_date_range(segment_id, start_date, end_date)
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}
    if result is None:
        return {"message": "No data available for this segment in the given date range"}
    return {"effort_counts": result}


@app.get("/segments_stats/{location}")
async def segments_stats(request: Request, location: str, start_date: str, end_date: str):
    """Get effort counts for all segments in a specific location within a date range."""
    segment_ids = segment_ids_dict.get(location)
    if not segment_ids:
        raise HTTPException(status_code=404, detail="Location not found")
    try:
        db = Database(config)
        segments_repository = SegmentsRepository(db, config)
        data = {}
        for segment_id in segment_ids.keys():
            segment = segments_repository.get_segment(segment_id)
            result = segments_repository.get_effort_counts_for_date_range(segment_id, start_date, end_date)
            if result is not None:
                data[segment_id] = {"name": segment.name, "efforts": result}
        return templates.TemplateResponse("stats.html", {"request": request, "data": data})
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}
