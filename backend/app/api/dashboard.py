from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.dashboard import DashboardStats
from app.services.dashboard_service import DashboardService
from app.api.auth import get_current_user_optional

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@dashboard_router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics."""
    return DashboardService.get_dashboard_stats(db)


@dashboard_router.get("/recent-activity")
def get_recent_activity(
    limit: int = 10,
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get recent activity across the system."""
    return DashboardService.get_recent_activity(db, limit=limit)
