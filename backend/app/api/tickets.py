from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.maintenance_ticket import MaintenanceTicketResponse, MaintenanceTicketUpdate
from app.services.ticket_service import TicketService
from app.api.auth import get_current_user_optional

tickets_router = APIRouter(prefix="/api/tickets", tags=["Tickets"])


@tickets_router.get("", response_model=List[MaintenanceTicketResponse])
def get_tickets(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    assigned_team: Optional[str] = Query(None, description="Filter by assigned team"),
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get all maintenance tickets with optional filtering."""
    return TicketService.get_tickets(
        db,
        skip=skip,
        limit=limit,
        status=status,
        priority=priority,
        assigned_team=assigned_team
    )


@tickets_router.get("/{ticket_id}", response_model=MaintenanceTicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific ticket by ID."""
    ticket = TicketService.get_ticket_by_db_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@tickets_router.patch("/{ticket_id}", response_model=MaintenanceTicketResponse)
def update_ticket(
    ticket_id: int,
    update_data: MaintenanceTicketUpdate,
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Update a ticket."""
    ticket = TicketService.update_ticket(db, ticket_id, update_data)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@tickets_router.post("/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    team: str,
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Assign a ticket to a team."""
    user_id = current_user.id if current_user else 1
    ticket = TicketService.assign_ticket(db, ticket_id, team, user_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket assigned", "ticket": ticket}


@tickets_router.post("/{ticket_id}/resolve")
def resolve_ticket(
    ticket_id: int,
    resolution_notes: str,
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Mark a ticket as resolved."""
    user_id = current_user.id if current_user else 1
    ticket = TicketService.resolve_ticket(db, ticket_id, resolution_notes, user_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket resolved", "ticket": ticket}


@tickets_router.post("/{ticket_id}/close")
def close_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    """Close a ticket."""
    ticket = TicketService.close_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket closed", "ticket": ticket}


@tickets_router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    """Delete a ticket."""
    success = TicketService.delete_ticket(db, ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted successfully"}
