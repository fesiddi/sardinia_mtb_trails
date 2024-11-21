from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse

from app.db.database import DatabaseConnectionError
from app.models.trail_area import TrailArea, TrailBase
from app.services.areas_repository import AreasRepository
from app.services.areas_service import get_areas_repository
from app.utils.logger import Logger

router = APIRouter()


@router.get("/trail-areas", tags=["areas"], response_model=List[TrailArea])
def trail_areas(areas_repository: AreasRepository = Depends(get_areas_repository)):
    """Get all trail areas."""
    try:
        found_areas = areas_repository.get_all_areas()
        return found_areas
    except DatabaseConnectionError as e:
        return {"message": f"Error getting trail areas from db: {e}"}


@router.get("/trail-areas/{name}", response_model=TrailArea)
def trail_area(name, areas_repository: AreasRepository = Depends(get_areas_repository)):
    """Get trail area data for a specific area."""
    try:
        area = areas_repository.get_area(name)
        if not area:
            raise HTTPException(status_code=404, detail="Area not found")
        return area
    except DatabaseConnectionError as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting trail area from db: {e}"
        )


@router.post("/trail-areas", response_model=TrailArea)
def add_area(
    area: TrailArea, areas_repository: AreasRepository = Depends(get_areas_repository)
):
    """Add a new trail area to the database."""
    try:
        Logger.info(f"Adding trail area {area.name}")
        new_area = areas_repository.add_area(area)
        return new_area
    except DatabaseConnectionError as e:
        return {"message": f"Error adding trail area in db: {e}"}


@router.put("/trail-areas/{name}", response_model=TrailArea)
def edit_area(
    name,
    area: TrailArea,
    areas_repository: AreasRepository = Depends(get_areas_repository),
) -> Response:
    """Edit an existing trail area in the database."""
    try:
        Logger.info(f"Editing trail area: {name}")
        edited_area = areas_repository.edit_area(name, area)
        return edited_area
    except DatabaseConnectionError as e:
        return {"message": f"Error editing trail area in db: {e}"}


@router.delete("/trail-areas/{name}")
def delete_area(
    name, areas_repository: AreasRepository = Depends(get_areas_repository)
) -> JSONResponse:
    """Delete an existing trail area from the database."""
    try:
        Logger.info(f"Deleting trail area: {name}")
        areas_repository.delete_area(name)
        return JSONResponse(content={"message": "Area deleted"})
    except DatabaseConnectionError as e:
        return JSONResponse(
            content={"message": f"Error deleting trail area from db: {e}"}
        )


@router.post("/trail-areas/{name}/trail_bases")
def add_trail_base_to_area(
    name: str,
    trail_base: TrailBase,
    areas_repository: AreasRepository = Depends(get_areas_repository),
) -> JSONResponse:
    """Add a new trail base to a trail area."""
    try:
        Logger.info(f"Adding trail base to area: {name}")
        areas_repository.add_trail_base_to_area(name, trail_base.model_dump())
        return JSONResponse(content={"message": "Trail base added"})
    except DatabaseConnectionError as e:
        return JSONResponse(content={"message": f"Error adding trail base in db: {e}"})
