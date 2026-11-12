from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InspectionBase(BaseModel):
    road_name: Optional[str] = None
    area: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    ward: Optional[str] = None
    zone: Optional[str] = None
    notes: Optional[str] = None


class InspectionCreate(InspectionBase):
    pass


class InspectionUpdate(BaseModel):
    status: Optional[str] = None
    processing_progress: Optional[float] = None


class InspectionResponse(InspectionBase):
    id: int
    filename: str
    file_path: str
    upload_date: datetime
    uploaded_by: int
    status: str
    processing_progress: float
    total_frames: int
    duration: float
    
    class Config:
        from_attributes = True
