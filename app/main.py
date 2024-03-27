import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .segments import get_segment, get_segment_raw_data, segment_ids_map
from .segments_stats import fetch_and_write_segments_stats
from .trail_areas_data import trail_areas_data

load_dotenv()

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)
templates = Jinja2Templates(directory="app/static/templates")


@app.get("/")
async def segment_list(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "trail_areas_data": trail_areas_data}
    )


@app.get("/segments/{location}")
async def segments_location(location):
    """Get all mapped segments for a specific location."""
    segment_ids = segment_ids_map.get(location)

    if not segment_ids:
        raise HTTPException(status_code=404, detail="Location not found")

    return [get_segment(segment_id) for segment_id in segment_ids.keys()]


@app.get("/raw_segment/{segment_id}")
async def raw_segment(segment_id):
    """Get raw data for a specific segment."""
    return get_segment_raw_data(segment_id)


@app.get("/fetch_segment_stats")
async def fetch_segment_stats_route():
    try:
        fetch_and_write_segments_stats()
    except Exception as e:
        return {"message": f"Error fetching segment stats: {e}"}

    return {"message": "Segment stats fetched successfully"}
