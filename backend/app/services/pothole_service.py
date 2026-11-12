import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.pothole import Pothole
from app.schemas.pothole import PotholeCreate, PotholeMapResponse
from app.models.maintenance_ticket import MaintenanceTicket


class PotholeService:
    """Handle pothole-related operations."""
    
    @staticmethod
    def create_pothole(db: Session, pothole_data: PotholeCreate) -> Pothole:
        """Create a new pothole record."""
        db_pothole = Pothole(
            inspection_id=pothole_data.inspection_id,
            timestamp=pothole_data.timestamp,
            frame_number=pothole_data.frame_number,
            latitude=pothole_data.latitude,
            longitude=pothole_data.longitude,
            confidence=pothole_data.confidence,
            severity=pothole_data.severity,
            image_path=pothole_data.image_path,
            bbox=pothole_data.bbox,
            status=pothole_data.status,
            road_name=pothole_data.road_name,
            area=pothole_data.area,
            detection_metadata=pothole_data.detection_metadata
        )
        db.add(db_pothole)
        db.commit()
        db.refresh(db_pothole)
        return db_pothole
    
    @staticmethod
    def get_pothole(db: Session, pothole_id: int) -> Optional[Pothole]:
        """Get a pothole by ID."""
        return db.query(Pothole).filter(Pothole.id == pothole_id).first()
    
    @staticmethod
    def get_potholes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        inspection_id: Optional[int] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        area: Optional[str] = None
    ) -> List[Pothole]:
        """Get potholes with optional filtering."""
        query = db.query(Pothole)
        
        if inspection_id:
            query = query.filter(Pothole.inspection_id == inspection_id)
        if severity:
            query = query.filter(Pothole.severity == severity)
        if status:
            query = query.filter(Pothole.status == status)
        if area:
            query = query.filter(Pothole.area == area)
        
        return query.order_by(Pothole.timestamp.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_potholes_for_map(
        db: Session,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        area: Optional[str] = None
    ) -> List[PotholeMapResponse]:
        """Get potholes formatted for map display."""
        query = db.query(Pothole)
        
        if severity:
            query = query.filter(Pothole.severity == severity)
        if status:
            query = query.filter(Pothole.status == status)
        if area:
            query = query.filter(Pothole.area == area)
        
        potholes = query.all()
        
        # Format for map response
        map_responses = []
        for pothole in potholes:
            # Get ticket info if exists
            ticket = db.query(MaintenanceTicket).filter(
                MaintenanceTicket.pothole_id == pothole.id
            ).first()
            
            map_response = PotholeMapResponse(
                id=pothole.id,
                latitude=pothole.latitude or 0.0,
                longitude=pothole.longitude or 0.0,
                severity=pothole.severity,
                confidence=pothole.confidence,
                status=pothole.status,
                ticket_id=ticket.ticket_id if ticket else None,
                detection_time=pothole.inspection.upload_date if pothole.inspection else None
            )
            map_responses.append(map_response)
        
        return map_responses
    
    @staticmethod
    def update_pothole_status(db: Session, pothole_id: int, status: str) -> Optional[Pothole]:
        """Update pothole status."""
        db_pothole = PotholeService.get_pothole(db, pothole_id)
        if not db_pothole:
            return None
        
        db_pothole.status = status
        db.commit()
        db.refresh(db_pothole)
        return db_pothole
    
    @staticmethod
    def delete_pothole(db: Session, pothole_id: int) -> bool:
        """Delete a pothole."""
        db_pothole = PotholeService.get_pothole(db, pothole_id)
        if not db_pothole:
            return False
        
        # Delete associated image if exists
        if db_pothole.image_path:
            import os
            try:
                if os.path.exists(db_pothole.image_path):
                    os.remove(db_pothole.image_path)
            except Exception as e:
                print(f"Error deleting image: {e}")
        
        db.delete(db_pothole)
        db.commit()
        return True
    
    @staticmethod
    def get_pothole_stats(db: Session) -> dict:
        """Get pothole statistics."""
        total = db.query(Pothole).count()
        critical = db.query(Pothole).filter(Pothole.severity == "Critical").count()
        high = db.query(Pothole).filter(Pothole.severity == "High").count()
        medium = db.query(Pothole).filter(Pothole.severity == "Medium").count()
        low = db.query(Pothole).filter(Pothole.severity == "Low").count()
        
        # Average confidence
        avg_confidence = 0.0
        if total > 0:
            confidences = [p.confidence for p in db.query(Pothole).all()]
            avg_confidence = sum(confidences) / len(confidences)
        
        return {
            "total": total,
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
            "average_confidence": avg_confidence
        }
    
    @staticmethod
    def get_potholes_by_severity(db: Session) -> dict:
        """Get pothole count by severity."""
        from sqlalchemy import func
        result = db.query(
            Pothole.severity,
            func.count(Pothole.id)
        ).group_by(Pothole.severity).all()
        
        return {severity: count for severity, count in result}
    
    @staticmethod
    def get_potholes_by_area(db: Session) -> dict:
        """Get pothole count by area."""
        from sqlalchemy import func
        result = db.query(
            Pothole.area,
            func.count(Pothole.id)
        ).filter(Pothole.area.isnot(None)).group_by(Pothole.area).all()
        
        return {area: count for area, count in result}
