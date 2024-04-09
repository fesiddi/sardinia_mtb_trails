from fastapi import APIRouter, Depends, HTTPException

from app.models.TrailArea import TrailArea, TrailBase
from app.services.areas_repository import AreasRepository
from app.db.database import DatabaseConnectionError
from app.services.areas_service import get_areas_repository
from app.utils.logger import Logger

router = APIRouter()


@router.get("/trail_areas", tags=["areas"])
def trail_areas(areas_repository: AreasRepository = Depends(get_areas_repository)):
    """Get all trail areas."""
    try:
        found_areas = areas_repository.get_all_areas()
        return found_areas
    except DatabaseConnectionError as e:
        return {"message": f"Error getting trail areas from db: {e}"}
    except Exception as e:
        return {"message": f"Error getting areas: {e}"}


@router.get("/trail_areas/{name}")
def trail_area(name, areas_repository: AreasRepository = Depends(get_areas_repository)):
    """Get trail area data for a specific area."""
    try:
        area = areas_repository.get_area(name)
        if not area:
            raise HTTPException(status_code=404, detail="Area not found")
        return area
    except DatabaseConnectionError as e:
        return {"message": f"Error getting trail area from db: {e}"}
    except Exception as e:
        return {"message": f"Error getting trail area: {e}"}


@router.post("/trail_areas")
def add_area(area: dict, areas_repository: AreasRepository = Depends(get_areas_repository)):
    """Add a new trail area to the database."""
    try:
        validated_area = TrailArea(**area)
        Logger.info(f"Adding trail area {validated_area.name}")
        new_area = areas_repository.add_area(validated_area)
        return new_area
    except DatabaseConnectionError as e:
        return {"message": f"Error adding trail area in db: {e}"}
    except Exception as e:
        return {"message": f"Error adding trail area: {e}"}


@router.put("/trail_areas/{name}")
def edit_area(name, area: dict, areas_repository: AreasRepository = Depends(get_areas_repository)):
    """Edit an existing trail area in the database."""
    try:
        Logger.info(f"Editing trail area: {name}")
        validated_area = TrailArea(**area)
        edited_area = areas_repository.edit_area(name, validated_area)
        return edited_area
    except DatabaseConnectionError as e:
        return {"message": f"Error editing trail area in db: {e}"}
    except Exception as e:
        return {"message": f"Error editing trail area: {e}"}


@router.delete("/trail_areas/{name}")
def delete_area(name, areas_repository: AreasRepository = Depends(get_areas_repository)):
    """Delete an existing trail area from the database."""
    try:
        Logger.info(f"Deleting trail area: {name}")
        areas_repository.delete_area(name)
        return {"message": "Area deleted"}
    except DatabaseConnectionError as e:
        return {"message": f"Error deleting trail area from db: {e}"}
    except Exception as e:
        return {"message": f"Error deleting trail area: {e}"}


@router.post("/trail_areas/{name}/trail_bases")
def add_trail_base_to_area(
    name: str,
    trail_base: TrailBase,
    areas_repository: AreasRepository = Depends(get_areas_repository)
):
    """Add a new trail base to a trail area."""
    try:
        Logger.info(f"Adding trail base to area: {name}")
        areas_repository.add_trail_base_to_area(name, trail_base.dict())
        return {"message": "Trail base added"}
    except DatabaseConnectionError as e:
        return {"message": f"Error adding trail base in db: {e}"}
    except Exception as e:
        return {"message": f"Error adding trail base: {e}"}
