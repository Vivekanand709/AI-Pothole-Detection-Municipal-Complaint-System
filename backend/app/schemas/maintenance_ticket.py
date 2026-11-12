from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MaintenanceTicketBase(BaseModel):
    priority: str
    description: Optional[str] = None
    assigned_team: Optional[str] = None


class MaintenanceTicketCreate(MaintenanceTicketBase):
    pothole_id: int


class MaintenanceTicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_team: Optional[str] = None
    resolution_notes: Optional[str] = None
    priority: Optional[str] = None


class MaintenanceTicketResponse(MaintenanceTicketBase):
    id: int
    ticket_id: str
    pothole_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    
    class Config:
        from_attributes = True
