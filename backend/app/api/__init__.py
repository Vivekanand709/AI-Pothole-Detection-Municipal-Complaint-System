from app.api.auth import auth_router
from app.api.inspections import inspections_router
from app.api.potholes import potholes_router
from app.api.tickets import tickets_router
from app.api.dashboard import dashboard_router

__all__ = [
    "auth_router",
    "inspections_router",
    "potholes_router",
    "tickets_router",
    "dashboard_router"
]
