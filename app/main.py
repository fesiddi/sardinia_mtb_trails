import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from cachetools import TTLCache, cached
from app.segments_data.segment_ids import segment_ids_dict
from app.services.strava_api import StravaApi
from app.services.segment_stats_dao import SegmentStatsDAO
from app.segments_data.trail_areas_data import trail_areas_data
from app.db.database import Database, DatabaseConnectionError

load_dotenv()

app = FastAPI()

cache = TTLCache(maxsize=1024, ttl=43200)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)
templates = Jinja2Templates(directory="app/static/templates")

strava_api = StravaApi()


@app.get("/")
async def home_route(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "trail_areas_data": trail_areas_data}
    )


@cached(cache)
@app.get("/segments/{location}")
async def segments_location(location):
    """Get all mapped segments for a specific location."""
    segment_ids = segment_ids_dict.get(location)

    if not segment_ids:
        raise HTTPException(status_code=404, detail="Location not found")

    # Use the StravaApi instance to get the segment data
    return [strava_api.get_segment(segment_id) for segment_id in segment_ids.keys()]


@app.get("/raw_segment/{segment_id}")
async def raw_segment(segment_id):
    """Get raw data for a specific segment."""
    # Use the StravaApi instance to get the raw segment data
    return strava_api.get_segment_raw_data(segment_id)


@app.get("/effort_change/{segment_id}")
async def effort_change(segment_id):
    """Get effort change for a specific segment if second parameter is not provided, it will default to 7 days."""
    try:
        db = Database()
        dao = SegmentStatsDAO(db)
        result = dao.get_effort_count_change_for_last_x_days(segment_id)
    except DatabaseConnectionError as e:
        return {"message": f"Error fetching segment stats: {e}"}
    if result is None:
        return {"message": "No data available for this segment"}
    return result
