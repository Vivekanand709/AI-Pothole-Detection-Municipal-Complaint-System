from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.pothole import PotholeResponse, PotholeMapResponse
from app.services.pothole_service import PotholeService
from app.api.auth import get_current_user_optional

potholes_router = APIRouter(prefix="/api/potholes", tags=["Potholes"])


@potholes_router.get("", response_model=List[PotholeResponse])
def get_potholes(
    skip: int = 0,
    limit: int = 100,
    inspection_id: Optional[int] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    area: Optional[str] = None,
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get all potholes with optional filtering."""
    return PotholeService.get_potholes(
        db,
        skip=skip,
        limit=limit,
        inspection_id=inspection_id,
        severity=severity,
        status=status,
        area=area
    )


@potholes_router.get("/map", response_model=List[PotholeMapResponse])
def get_potholes_for_map(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    area: Optional[str] = Query(None, description="Filter by area"),
    db: Session = Depends(get_db)
):
    """Get potholes formatted for map display."""
    return PotholeService.get_potholes_for_map(
        db,
        severity=severity,
        status=status,
        area=area
    )


@potholes_router.get("/{pothole_id}", response_model=PotholeResponse)
def get_pothole(
    pothole_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific pothole by ID."""
    pothole = PotholeService.get_pothole(db, pothole_id)
    if not pothole:
        raise HTTPException(status_code=404, detail="Pothole not found")
    return pothole


@potholes_router.patch("/{pothole_id}/status")
def update_pothole_status(
    pothole_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update pothole status."""
    pothole = PotholeService.update_pothole_status(db, pothole_id, status)
    if not pothole:
        raise HTTPException(status_code=404, detail="Pothole not found")
    return {"message": "Status updated", "pothole": pothole}


@potholes_router.delete("/{pothole_id}")
def delete_pothole(
    pothole_id: int,
    db: Session = Depends(get_db)
):
    """Delete a pothole."""
    success = PotholeService.delete_pothole(db, pothole_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pothole not found")
    return {"message": "Pothole deleted successfully"}
