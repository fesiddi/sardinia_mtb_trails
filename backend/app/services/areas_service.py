from dotenv import load_dotenv
from fastapi import Depends, HTTPException

from app.db.database import Database, DatabaseConnectionError
from app.services.areas_repository import AreasRepository
from app.utils.config import Config

load_dotenv()

config = Config()


def get_db():
    try:
        db = Database(config)
        return db
    except DatabaseConnectionError:
        raise HTTPException(status_code=500, detail="Database connection error")


def get_areas_repository(db: Database = Depends(get_db)):
    return AreasRepository(db, config)
