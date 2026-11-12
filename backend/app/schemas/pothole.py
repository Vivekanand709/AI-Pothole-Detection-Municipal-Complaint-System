from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PotholeBase(BaseModel):
    inspection_id: int
    timestamp: float
    frame_number: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    confidence: float
    severity: str
    image_path: Optional[str] = None
    bbox: str
    status: str = "detected"
    road_name: Optional[str] = None
    area: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    ward: Optional[str] = None
    zone: Optional[str] = None
    detection_metadata: Optional[str] = None


class PotholeCreate(PotholeBase):
    pass


class PotholeResponse(PotholeBase):
    id: int
    detection_metadata: Optional[str] = None
    
    class Config:
        from_attributes = True


class PotholeMapResponse(BaseModel):
    id: int
    latitude: float
    longitude: float
    severity: str
    confidence: float
    status: str
    ticket_id: Optional[str] = None
    detection_time: datetime
    
    class Config:
        from_attributes = True
