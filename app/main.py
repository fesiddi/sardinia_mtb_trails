import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .segment_ids import segment_ids_dict
from .segment_stats_dao import SegmentStatsDAO
from .segments import get_segment, get_segment_raw_data
from .segments_stats import fetch_and_write_segments_stats, get_effort_count_change_for_last_x_days
from .trail_areas_data import trail_areas_data
from .database import Database, DatabaseConnectionError

load_dotenv()

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)
templates = Jinja2Templates(directory="app/static/templates")


@app.get("/")
async def home_route(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "trail_areas_data": trail_areas_data}
    )


@app.get("/segments/{location}")
async def segments_location(location):
    """Get all mapped segments for a specific location."""
    segment_ids = segment_ids_dict.get(location)

    if not segment_ids:
        raise HTTPException(status_code=404, detail="Location not found")

    return [get_segment(segment_id) for segment_id in segment_ids.keys()]


@app.get("/raw_segment/{segment_id}")
async def raw_segment(segment_id):
    """Get raw data for a specific segment."""
    return get_segment_raw_data(segment_id)


@app.get("/effort_change/{segment_id}")
async def effort_change(segment_id):
    """Get effort change for a specific segment."""
    try:
        db = Database()
        dao = SegmentStatsDAO(db)
        result = get_effort_count_change_for_last_x_days(dao, segment_id)
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}
    if result is None:
        return {"message": "No data available for this segment"}
    return result


@app.get("/update_segments_effort_stats")
async def update_segments_effort_stats():
    """Update segment stats in the database."""
    try:
        db = Database()
        dao = SegmentStatsDAO(db)
        fetch_and_write_segments_stats(dao)
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}

    return {"message": "Segment stats updated successfully"}
