from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.maintenance_ticket import MaintenanceTicket
from app.schemas.maintenance_ticket import MaintenanceTicketCreate, MaintenanceTicketUpdate
from app.models.user import User


class TicketService:
    """Handle maintenance ticket operations."""
    
    @staticmethod
    def create_ticket(db: Session, ticket_data: MaintenanceTicketCreate) -> MaintenanceTicket:
        """Create a new maintenance ticket."""
        db_ticket = MaintenanceTicket(
            ticket_id=ticket_data.ticket_id,
            pothole_id=ticket_data.pothole_id,
            priority=ticket_data.priority,
            status="Open",
            description=ticket_data.description,
            assigned_team=ticket_data.assigned_team
        )
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    
    @staticmethod
    def create_ticket_from_dict(db: Session, ticket_dict: dict) -> MaintenanceTicket:
        """Create a ticket from a dictionary (used by AI pipeline)."""
        db_ticket = MaintenanceTicket(
            ticket_id=ticket_dict.get("ticket_id"),
            pothole_id=ticket_dict.get("pothole_id"),
            priority=ticket_dict.get("priority"),
            status=ticket_dict.get("status", "Open"),
            description=ticket_dict.get("description"),
            assigned_team=ticket_dict.get("assigned_team"),
            created_at=ticket_dict.get("created_at", datetime.now())
        )
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    
    @staticmethod
    def get_ticket(db: Session, ticket_id: str) -> Optional[MaintenanceTicket]:
        """Get a ticket by ID."""
        return db.query(MaintenanceTicket).filter(MaintenanceTicket.ticket_id == ticket_id).first()
    
    @staticmethod
    def get_ticket_by_db_id(db: Session, ticket_id: int) -> Optional[MaintenanceTicket]:
        """Get a ticket by database ID."""
        return db.query(MaintenanceTicket).filter(MaintenanceTicket.id == ticket_id).first()
    
    @staticmethod
    def get_tickets(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_team: Optional[str] = None
    ) -> List[MaintenanceTicket]:
        """Get tickets with optional filtering."""
        query = db.query(MaintenanceTicket)
        
        if status:
            query = query.filter(MaintenanceTicket.status == status)
        if priority:
            query = query.filter(MaintenanceTicket.priority == priority)
        if assigned_team:
            query = query.filter(MaintenanceTicket.assigned_team == assigned_team)
        
        return query.order_by(MaintenanceTicket.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_ticket(
        db: Session,
        ticket_id: int,
        update_data: MaintenanceTicketUpdate
    ) -> Optional[MaintenanceTicket]:
        """Update a ticket."""
        db_ticket = TicketService.get_ticket_by_db_id(db, ticket_id)
        if not db_ticket:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        
        # Handle status-specific updates
        if "status" in update_dict:
            new_status = update_dict["status"]
            if new_status == "Resolved" and db_ticket.status != "Resolved":
                db_ticket.resolved_at = datetime.now()
            elif new_status != "Resolved":
                db_ticket.resolved_at = None
        
        for key, value in update_dict.items():
            setattr(db_ticket, key, value)
        
        db_ticket.updated_at = datetime.now()
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    
    @staticmethod
    def assign_ticket(db: Session, ticket_id: int, team: str, user_id: int) -> Optional[MaintenanceTicket]:
        """Assign a ticket to a team."""
        db_ticket = TicketService.get_ticket_by_db_id(db, ticket_id)
        if not db_ticket:
            return None
        
        db_ticket.assigned_team = team
        db_ticket.status = "Assigned"
        db_ticket.resolved_by = user_id
        db_ticket.updated_at = datetime.now()
        
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    
    @staticmethod
    def resolve_ticket(db: Session, ticket_id: int, resolution_notes: str, user_id: int) -> Optional[MaintenanceTicket]:
        """Mark a ticket as resolved."""
        db_ticket = TicketService.get_ticket_by_db_id(db, ticket_id)
        if not db_ticket:
            return None
        
        db_ticket.status = "Resolved"
        db_ticket.resolution_notes = resolution_notes
        db_ticket.resolved_at = datetime.now()
        db_ticket.resolved_by = user_id
        db_ticket.updated_at = datetime.now()
        
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    
    @staticmethod
    def close_ticket(db: Session, ticket_id: int) -> Optional[MaintenanceTicket]:
        """Close a ticket."""
        db_ticket = TicketService.get_ticket_by_db_id(db, ticket_id)
        if not db_ticket:
            return None
        
        db_ticket.status = "Closed"
        db_ticket.updated_at = datetime.now()
        
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    
    @staticmethod
    def delete_ticket(db: Session, ticket_id: int) -> bool:
        """Delete a ticket."""
        db_ticket = TicketService.get_ticket_by_db_id(db, ticket_id)
        if not db_ticket:
            return False
        
        db.delete(db_ticket)
        db.commit()
        return True
    
    @staticmethod
    def get_ticket_stats(db: Session) -> dict:
        """Get ticket statistics."""
        total = db.query(MaintenanceTicket).count()
        open_tickets = db.query(MaintenanceTicket).filter(MaintenanceTicket.status == "Open").count()
        assigned = db.query(MaintenanceTicket).filter(MaintenanceTicket.status == "Assigned").count()
        in_progress = db.query(MaintenanceTicket).filter(MaintenanceTicket.status == "In Progress").count()
        resolved = db.query(MaintenanceTicket).filter(MaintenanceTicket.status == "Resolved").count()
        closed = db.query(MaintenanceTicket).filter(MaintenanceTicket.status == "Closed").count()
        
        return {
            "total": total,
            "open": open_tickets,
            "assigned": assigned,
            "in_progress": in_progress,
            "resolved": resolved,
            "closed": closed
        }
    
    @staticmethod
    def get_tickets_by_status(db: Session) -> dict:
        """Get ticket count by status."""
        from sqlalchemy import func
        result = db.query(
            MaintenanceTicket.status,
            func.count(MaintenanceTicket.id)
        ).group_by(MaintenanceTicket.status).all()
        
        return {status: count for status, count in result}
