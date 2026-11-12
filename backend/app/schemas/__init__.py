from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.inspection import InspectionCreate, InspectionResponse, InspectionUpdate
from app.schemas.pothole import PotholeResponse, PotholeCreate, PotholeMapResponse
from app.schemas.maintenance_ticket import MaintenanceTicketCreate, MaintenanceTicketResponse, MaintenanceTicketUpdate
from app.schemas.dashboard import DashboardStats

__all__ = [
    "UserCreate", "UserLogin", "UserResponse",
    "InspectionCreate", "InspectionResponse", "InspectionUpdate",
    "PotholeResponse", "PotholeCreate", "PotholeMapResponse",
    "MaintenanceTicketCreate", "MaintenanceTicketResponse", "MaintenanceTicketUpdate",
    "DashboardStats"
]
