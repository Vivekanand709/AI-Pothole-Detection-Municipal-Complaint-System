import os
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.inspection import Inspection
from app.models.pothole import Pothole
from app.schemas.inspection import InspectionCreate, InspectionUpdate
from app.config import settings


class InspectionService:
    """Handle inspection-related operations."""
    
    @staticmethod
    def create_inspection(
        db: Session,
        filename: str,
        file_path: str,
        uploaded_by: int,
        inspection_data: InspectionCreate
    ) -> Inspection:
        """Create a new inspection record."""
        db_inspection = Inspection(
            filename=filename,
            file_path=file_path,
            uploaded_by=uploaded_by,
            road_name=inspection_data.road_name,
            area=inspection_data.area,
            state=inspection_data.state,
            district=inspection_data.district,
            city=inspection_data.city,
            ward=inspection_data.ward,
            zone=inspection_data.zone,
            notes=inspection_data.notes,
            status="uploaded",
            processing_progress=0.0
        )
        db.add(db_inspection)
        db.commit()
        db.refresh(db_inspection)
        return db_inspection
    
    @staticmethod
    def get_inspection(db: Session, inspection_id: int) -> Optional[Inspection]:
        """Get an inspection by ID."""
        return db.query(Inspection).filter(Inspection.id == inspection_id).first()
    
    @staticmethod
    def get_inspections(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None
    ) -> List[Inspection]:
        """Get all inspections with optional filtering."""
        query = db.query(Inspection)
        if user_id:
            query = query.filter(Inspection.uploaded_by == user_id)
        return query.order_by(Inspection.upload_date.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_inspection(
        db: Session,
        inspection_id: int,
        update_data: InspectionUpdate
    ) -> Optional[Inspection]:
        """Update an inspection."""
        db_inspection = InspectionService.get_inspection(db, inspection_id)
        if not db_inspection:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_inspection, key, value)
        
        db.commit()
        db.refresh(db_inspection)
        return db_inspection
    
    @staticmethod
    def update_progress(db: Session, inspection_id: int, progress: float) -> Optional[Inspection]:
        """Update inspection processing progress."""
        db_inspection = InspectionService.get_inspection(db, inspection_id)
        if not db_inspection:
            return None
        
        db_inspection.processing_progress = progress
        db.commit()
        db.refresh(db_inspection)
        return db_inspection
    
    @staticmethod
    def update_status(db: Session, inspection_id: int, status: str) -> Optional[Inspection]:
        """Update inspection status."""
        db_inspection = InspectionService.get_inspection(db, inspection_id)
        if not db_inspection:
            return None
        
        db_inspection.status = status
        db.commit()
        db.refresh(db_inspection)
        return db_inspection
    
    @staticmethod
    def delete_inspection(db: Session, inspection_id: int) -> bool:
        """Delete an inspection and its associated data."""
        db_inspection = InspectionService.get_inspection(db, inspection_id)
        if not db_inspection:
            return False
        
        # Delete associated potholes and their tickets
        potholes = db.query(Pothole).filter(Pothole.inspection_id == inspection_id).all()
        for pothole in potholes:
            # Delete associated ticket first
            if pothole.maintenance_ticket:
                db.delete(pothole.maintenance_ticket)
            # Then delete the pothole
            db.delete(pothole)
        
        # Delete associated file
        if os.path.exists(db_inspection.file_path):
            try:
                os.remove(db_inspection.file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")
        
        db.delete(db_inspection)
        db.commit()
        return True
    
    @staticmethod
    def get_inspection_stats(db: Session) -> dict:
        """Get inspection statistics."""
        total = db.query(Inspection).count()
        completed = db.query(Inspection).filter(Inspection.status == "completed").count()
        processing = db.query(Inspection).filter(Inspection.status == "processing").count()
        failed = db.query(Inspection).filter(Inspection.status == "failed").count()
        
        return {
            "total": total,
            "completed": completed,
            "processing": processing,
            "failed": failed
        }
