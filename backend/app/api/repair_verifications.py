import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.maintenance_ticket import MaintenanceTicket
from app.models.pothole import Pothole
from app.models.repair_verification import RepairVerification
from app.api.auth import get_current_user

verification_router = APIRouter(prefix="/api/tickets", tags=["Repair Verification"])
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads" / "repair_verifications"
MAX_IMAGE_SIZE = 8 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}


async def save_image(upload: UploadFile, label: str) -> str:
    if upload.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"{label} must be JPG, PNG, or WEBP.")
    data = await upload.read(MAX_IMAGE_SIZE + 1)
    if not data or len(data) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=413, detail=f"{label} must be a non-empty image up to 8 MB.")
    try:
        import io
        with Image.open(io.BytesIO(data)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail=f"{label} is not a valid image.")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ALLOWED_TYPES[upload.content_type]}"
    path = UPLOAD_DIR / filename
    path.write_bytes(data)
    return f"/uploads/repair_verifications/{filename}"


@verification_router.post("/{ticket_id}/verification", status_code=201)
async def submit_repair_verification(
    ticket_id: int,
    before_photo: UploadFile = File(...),
    after_photo: UploadFile = File(...),
    notes: Optional[str] = Form(None, max_length=2000),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Store before/after repair evidence and resolve the associated pothole ticket."""
    ticket = db.query(MaintenanceTicket).filter(MaintenanceTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Maintenance ticket not found.")
    before_path = await save_image(before_photo, "Before photo")
    try:
        after_path = await save_image(after_photo, "After photo")
        record = RepairVerification(
            ticket_id=ticket.id,
            before_image_path=before_path,
            after_image_path=after_path,
            notes=(notes or "").strip() or None,
            verified_by=current_user.id if current_user else None,
        )
        db.add(record)
        ticket.status = "Resolved"
        ticket.resolution_notes = (notes or "Repair evidence submitted").strip()
        from datetime import datetime
        ticket.resolved_at = datetime.now()
        if ticket.pothole:
            ticket.pothole.status = "resolved"
        db.commit()
        db.refresh(record)
        return {
            "id": record.id,
            "ticket_id": record.ticket_id,
            "before_image_url": record.before_image_path,
            "after_image_url": record.after_image_path,
            "notes": record.notes,
            "created_at": record.created_at,
            "status": ticket.status,
        }
    except Exception:
        db.rollback()
        for image_path in (before_path, locals().get("after_path")):
            if image_path:
                (UPLOAD_DIR / Path(image_path).name).unlink(missing_ok=True)
        raise


@verification_router.get("/{ticket_id}/verification")
def get_repair_verification(ticket_id: int, db: Session = Depends(get_db)):
    """Return repair evidence for a maintenance ticket."""
    ticket = db.query(MaintenanceTicket).filter(MaintenanceTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Maintenance ticket not found.")
    records = db.query(RepairVerification).filter(
        RepairVerification.ticket_id == ticket_id
    ).order_by(RepairVerification.created_at.desc()).all()
    return [{
        "id": item.id,
        "ticket_id": item.ticket_id,
        "before_image_url": item.before_image_path,
        "after_image_url": item.after_image_path,
        "notes": item.notes,
        "created_at": item.created_at,
    } for item in records]
