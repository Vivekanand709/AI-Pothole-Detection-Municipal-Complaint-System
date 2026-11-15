from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CitizenReportResponse(BaseModel):
    id: int
    complaint_code: str
    citizen_name: str
    description: str
    road_name: Optional[str] = None
    area: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_path: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
