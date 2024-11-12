from typing import List, Optional

from pydantic import BaseModel


class Effort(BaseModel):
    effort_count: int
    fetch_date: str


class SegmentEfforts(BaseModel):
    id: Optional[str] = None
    name: str
    efforts: List[Effort]

    @classmethod
    def from_mongo(cls, data: dict):
        id_str = str(data["_id"]) if "_id" in data else None
        return cls(
            id=id_str,
            name=data["name"],
            efforts=[
                Effort(effort_count=int(e["effort_count"]), fetch_date=e["fetch_date"])
                for e in data["efforts"]
            ],
        )
