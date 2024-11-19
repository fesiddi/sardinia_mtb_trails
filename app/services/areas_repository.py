from typing import List, Optional

from app.db.database import Database
from app.models.TrailArea import TrailArea
from app.utils.config import Config
from app.utils.logger import Logger


class AreasRepository:
    def __init__(self, db: Database, config: Config):
        self.config = config
        self.db = db

    def get_area(self, name: str) -> Optional[TrailArea]:
        """Get trail area data for a specific area."""
        Logger.debug(f"Getting area data for : {name}")
        result = self.db.find_one(self.config.AREAS_COLL_NAME, {"s_name": name})
        if result:
            return TrailArea(**result)
        return None

    def get_all_areas(self) -> List[TrailArea]:
        """Get all trail areas from the database."""
        Logger.debug("Getting all trail areas")
        result = self.db.find_many(self.config.AREAS_COLL_NAME, {})
        areas = [TrailArea(**doc) for doc in result]
        return areas

    def add_area(self, area: TrailArea) -> TrailArea:
        """Add a new trail area to the database."""
        Logger.debug(f"Adding new trail area: {area}")
        self.db.insert_one(self.config.AREAS_COLL_NAME, area.model_dump())
        return area

    def edit_area(self, name: str, area: TrailArea) -> TrailArea:
        """Edit an existing trail area in the database."""
        Logger.debug(f"Editing trail area: {name}")
        self.db.update_one(self.config.AREAS_COLL_NAME, {"s_name": name}, area.model_dump())
        return area

    def delete_area(self, name: str) -> bool:
        """Delete a trail area from the database."""
        Logger.debug(f"Deleting trail area: {name}")
        result = self.db.delete_one(self.config.AREAS_COLL_NAME, {"s_name": name})
        return result

    def add_trail_base_to_area(self, name: str, trail_base: dict) -> TrailArea:
        """Add a new trail base to a trail area."""
        Logger.debug(f"Adding trail base to area: {name}")
        self.db.update_one(
            self.config.AREAS_COLL_NAME,
            {"s_name": name},
            {"$push": {"trail_bases": trail_base}},
        )
        return self.get_area(name)
