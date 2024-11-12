import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import efforts, segments, trail_areas
from app.services.areas_repository import AreasRepository
from app.services.areas_service import get_areas_repository
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
async def home_route(
    request: Request, areas_repository: AreasRepository = Depends(get_areas_repository)
):
    try:
        trail_areas_data = areas_repository.get_all_areas()
        return templates.TemplateResponse(
            "index.html", {"request": request, "trail_areas_data": trail_areas_data}
        )
    except Exception as e:
        return {"message": f"Error loading home page: {e}"}


app.include_router(segments.router, tags=["segments"])
app.include_router(efforts.router, tags=["efforts"])
app.include_router(trail_areas.router, tags=["trail_areas"])
