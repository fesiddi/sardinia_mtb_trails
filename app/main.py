import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.segments_data.trail_areas_data import trail_areas_data
from app.utils.config import Config
from app.routes import segments, efforts

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


app.include_router(segments.router, tags=["segments"])
app.include_router(efforts.router, tags=["efforts"])
