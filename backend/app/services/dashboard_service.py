from typing import Dict, List, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.pothole import Pothole
from app.models.maintenance_ticket import MaintenanceTicket
from app.models.inspection import Inspection


class DashboardService:
    """Handle dashboard statistics and analytics."""
    
    @staticmethod
    def get_dashboard_stats(db: Session) -> Dict[str, Any]:
        """Get comprehensive dashboard statistics."""
        # Pothole statistics
        total_potholes = db.query(Pothole).count()
        critical_potholes = db.query(Pothole).filter(Pothole.severity == "Critical").count()
        high_severity_potholes = db.query(Pothole).filter(Pothole.severity == "High").count()
        
        # Ticket statistics
        open_tickets = db.query(MaintenanceTicket).filter(MaintenanceTicket.status == "Open").count()
        resolved_tickets = db.query(MaintenanceTicket).filter(MaintenanceTicket.status == "Resolved").count()
        
        # Inspection statistics
        videos_processed = db.query(Inspection).filter(Inspection.status == "completed").count()
        
        # Average confidence
        avg_confidence = 0.0
        if total_potholes > 0:
            confidences = db.query(Pothole.confidence).all()
            avg_confidence = sum([c[0] for c in confidences]) / len(confidences)
        
        # Potholes by severity
        potholes_by_severity = DashboardService._get_potholes_by_severity(db)
        
        # Potholes by area
        potholes_by_area = DashboardService._get_potholes_by_area(db)
        
        # Tickets by status
        tickets_by_status = DashboardService._get_tickets_by_status(db)
        
        # Potholes over time (last 30 days)
        potholes_over_time = DashboardService._get_potholes_over_time(db, days=30)
        
        return {
            "total_potholes": total_potholes,
            "critical_potholes": critical_potholes,
            "high_severity_potholes": high_severity_potholes,
            "open_tickets": open_tickets,
            "resolved_tickets": resolved_tickets,
            "videos_processed": videos_processed,
            "average_confidence": round(avg_confidence, 3),
            "potholes_by_severity": potholes_by_severity,
            "potholes_by_area": potholes_by_area,
            "tickets_by_status": tickets_by_status,
            "potholes_over_time": potholes_over_time
        }
    
    @staticmethod
    def _get_potholes_by_severity(db: Session) -> Dict[str, int]:
        """Get pothole count grouped by severity."""
        result = db.query(
            Pothole.severity,
            func.count(Pothole.id)
        ).group_by(Pothole.severity).all()
        
        severity_counts = {severity: count for severity, count in result}
        
        # Ensure all severities are present
        for severity in ["Low", "Medium", "High", "Critical"]:
            if severity not in severity_counts:
                severity_counts[severity] = 0
        
        return severity_counts
    
    @staticmethod
    def _get_potholes_by_area(db: Session) -> Dict[str, int]:
        """Get pothole count grouped by area."""
        result = db.query(
            Pothole.area,
            func.count(Pothole.id)
        ).filter(Pothole.area.isnot(None)).group_by(Pothole.area).all()
        
        return {area: count for area, count in result}
    
    @staticmethod
    def _get_tickets_by_status(db: Session) -> Dict[str, int]:
        """Get ticket count grouped by status."""
        result = db.query(
            MaintenanceTicket.status,
            func.count(MaintenanceTicket.id)
        ).group_by(MaintenanceTicket.status).all()
        
        status_counts = {status: count for status, count in result}
        
        # Ensure all statuses are present
        for status in ["Open", "Assigned", "In Progress", "Resolved", "Closed"]:
            if status not in status_counts:
                status_counts[status] = 0
        
        return status_counts
    
    @staticmethod
    def _get_potholes_over_time(db: Session, days: int = 30) -> List[Dict[str, Any]]:
        """Get pothole detection trend over time."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get potholes with their inspection dates
        result = db.query(
            func.date(Inspection.upload_date).label('date'),
            func.count(Pothole.id).label('count')
        ).join(Pothole, Inspection.id == Pothole.inspection_id)\
         .filter(Inspection.upload_date >= start_date)\
         .group_by(func.date(Inspection.upload_date))\
         .order_by(func.date(Inspection.upload_date))\
         .all()
        
        return [
            {
                "date": str(date),
                "count": count
            }
            for date, count in result
        ]
    
    @staticmethod
    def get_recent_activity(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activity across all entities."""
        activities = []
        
        # Recent inspections
        recent_inspections = db.query(Inspection)\
            .order_by(Inspection.upload_date.desc())\
            .limit(limit // 2)\
            .all()
        
        for inspection in recent_inspections:
            activities.append({
                "type": "inspection",
                "id": inspection.id,
                "description": f"Inspection '{inspection.filename}' uploaded",
                "timestamp": inspection.upload_date.isoformat(),
                "status": inspection.status
            })
        
        # Recent tickets
        recent_tickets = db.query(MaintenanceTicket)\
            .order_by(MaintenanceTicket.created_at.desc())\
            .limit(limit // 2)\
            .all()
        
        for ticket in recent_tickets:
            activities.append({
                "type": "ticket",
                "id": ticket.id,
                "description": f"Ticket {ticket.ticket_id} created",
                "timestamp": ticket.created_at.isoformat(),
                "status": ticket.status
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return activities[:limit]
