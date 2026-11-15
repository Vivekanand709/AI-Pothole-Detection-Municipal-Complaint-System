import io
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.citizen_report import CitizenReport
from app.schemas.citizen_report import CitizenReportResponse

citizen_reports_router = APIRouter(prefix="/api/citizen-reports", tags=["Citizen Reports"])

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads" / "citizen_reports"
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGE_SIZE = 8 * 1024 * 1024


@citizen_reports_router.post("", response_model=CitizenReportResponse, status_code=201)
async def create_citizen_report(
    citizen_name: str = Form(..., min_length=2, max_length=100),
    phone: str = Form(..., min_length=10, max_length=15),
    description: str = Form(..., min_length=10, max_length=2000),
    road_name: Optional[str] = Form(None, max_length=150),
    area: Optional[str] = Form(None, max_length=150),
    latitude: Optional[float] = Form(None, ge=-90, le=90),
    longitude: Optional[float] = Form(None, ge=-180, le=180),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Accept a citizen pothole report with a photo and optional GPS coordinates."""
    extension = Path(photo.filename or "").suffix.lower()
    if photo.content_type not in ALLOWED_IMAGE_TYPES or extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Upload a JPG, PNG, or WEBP image.")

    image_bytes = await photo.read(MAX_IMAGE_SIZE + 1)
    if not image_bytes:
        raise HTTPException(status_code=400, detail="The uploaded image is empty.")
    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=413, detail="Image must be 8 MB or smaller.")

    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid image.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}{extension}"
    destination = UPLOAD_DIR / stored_name
    destination.write_bytes(image_bytes)

    report = CitizenReport(
        complaint_code=f"RGA-{uuid.uuid4().hex[:12].upper()}",
        citizen_name=citizen_name.strip(),
        phone=phone.strip(),
        description=description.strip(),
        road_name=road_name.strip() if road_name else None,
        area=area.strip() if area else None,
        latitude=latitude,
        longitude=longitude,
        image_path=f"/uploads/citizen_reports/{stored_name}",
        status="Submitted",
    )
    try:
        db.add(report)
        db.commit()
        db.refresh(report)
        return report
    except Exception:
        db.rollback()
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Could not save the report. Please try again.")


@citizen_reports_router.get("/track/{complaint_code}")
def track_citizen_report(complaint_code: str, db: Session = Depends(get_db)):
    """Return complaint progress without exposing the citizen's contact details."""
    report = db.query(CitizenReport).filter(
        CitizenReport.complaint_code == complaint_code.upper()
    ).first()
    if not report:
        raise HTTPException(status_code=404, detail="No complaint found with this tracking code.")
    return {
        "complaint_code": report.complaint_code,
        "status": report.status,
        "description": report.description,
        "road_name": report.road_name,
        "area": report.area,
        "created_at": report.created_at,
    }
