from pydantic import BaseModel
from typing import List, Dict, Any


class DashboardStats(BaseModel):
    total_potholes: int
    critical_potholes: int
    high_severity_potholes: int
    open_tickets: int
    resolved_tickets: int
    videos_processed: int
    average_confidence: float
    potholes_by_severity: Dict[str, int]
    potholes_by_area: Dict[str, int]
    tickets_by_status: Dict[str, int]
    potholes_over_time: List[Dict[str, Any]]
