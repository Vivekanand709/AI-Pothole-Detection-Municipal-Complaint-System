import os
import uuid
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.inspection import InspectionCreate, InspectionResponse, InspectionUpdate
from app.services.inspection_service import InspectionService
from app.services.pothole_service import PotholeService
from app.services.ticket_service import TicketService
from app.ai.pipeline import Pipeline
from app.api.auth import get_current_user_optional
from app.config import settings
from app.models.pothole import Pothole

inspections_router = APIRouter(prefix="/api/inspections", tags=["Inspections"])


def process_inspection_background(
    inspection_id: int,
    video_path: str,
    output_dir: str,
    db: Session,
    road_name: Optional[str],
    area: Optional[str]
):
    """Background task to process inspection video."""
    try:
        # Update status to processing
        InspectionService.update_status(db, inspection_id, "processing")
        
        # Get inspection to access municipal fields
        inspection = InspectionService.get_inspection(db, inspection_id)
        if not inspection:
            print(f"Inspection {inspection_id} not found")
            InspectionService.update_status(db, inspection_id, "failed")
            return
        
        # Create pipeline
        pipeline = Pipeline(
            video_path=video_path,
            output_dir=output_dir,
            demo_mode=settings.DEMO_MODE,
            progress_callback=lambda progress, msg: InspectionService.update_progress(db, inspection_id, progress)
        )
        
        # Process video
        result = pipeline.process(
            frame_interval=30,
            road_name=road_name,
            area=area
        )
        
        if not result["success"]:
            InspectionService.update_status(db, inspection_id, "failed")
            return
        
        # Save detections to database
        detections = result["detections"]
        tickets_data = result["tickets"]
        
        # Check if potholes already exist for this inspection to prevent duplicates
        existing_potholes = db.query(Pothole).filter(Pothole.inspection_id == inspection_id).count()
        if existing_potholes > 0:
            print(f"Inspection {inspection_id} already has {existing_potholes} potholes. Skipping duplicate creation.")
            InspectionService.update_status(db, inspection_id, "completed")
            InspectionService.update_progress(db, inspection_id, 100.0)
            return
        
        for detection in detections:
            from app.schemas.pothole import PotholeCreate
            pothole_create = PotholeCreate(
                inspection_id=inspection_id,
                timestamp=detection["timestamp"],
                frame_number=detection["frame_number"],
                latitude=detection["latitude"],
                longitude=detection["longitude"],
                confidence=detection["confidence"],
                severity=detection["severity"],
                image_path=detection["frame_path"],
                bbox=str(detection["bbox"]),
                status="detected",
                road_name=detection.get("road_name"),
                area=detection.get("area"),
                state=inspection.state,
                district=inspection.district,
                city=inspection.city,
                ward=inspection.ward,
                zone=inspection.zone,
                detection_metadata=detection.get("detection_metadata")
            )
            pothole = PotholeService.create_pothole(db, pothole_create)
            
            # Create ticket for this pothole
            # Update ticket data with actual pothole ID
            ticket_idx = detections.index(detection)
            if ticket_idx < len(tickets_data):
                ticket_dict = tickets_data[ticket_idx]
                ticket_dict["pothole_id"] = pothole.id
                TicketService.create_ticket_from_dict(db, ticket_dict)
        
        # Update status to completed
        InspectionService.update_status(db, inspection_id, "completed")
        InspectionService.update_progress(db, inspection_id, 100.0)
        
    except Exception as e:
        print(f"Error processing inspection: {e}")
        InspectionService.update_status(db, inspection_id, "failed")


@inspections_router.post("/upload", response_model=InspectionResponse)
async def upload_inspection(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    road_name: Optional[str] = Form(None),
    area: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    district: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    ward: Optional[str] = Form(None),
    zone: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Upload a road inspection video."""
    # Validate file extension
    file_ext = os.path.splitext(video.filename)[1].lower()
    if file_ext not in settings.ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_VIDEO_EXTENSIONS)}"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    upload_dir = "backend/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Create inspection record
    inspection_data = InspectionCreate(
        road_name=road_name,
        area=area,
        state=state,
        district=district,
        city=city,
        ward=ward,
        zone=zone,
        notes=notes
    )
    
    # Use current user
    user_id = current_user.id if current_user else 1
    
    inspection = InspectionService.create_inspection(
        db,
        filename=video.filename,
        file_path=file_path,
        uploaded_by=user_id,
        inspection_data=inspection_data
    )
    
    # Start background processing (with duplicate protection in background task)
    output_dir = os.path.join("backend/detections", str(inspection.id))
    os.makedirs(output_dir, exist_ok=True)
    
    background_tasks.add_task(
        process_inspection_background,
        inspection.id,
        file_path,
        output_dir,
        db,
        road_name,
        area
    )
    
    return inspection


@inspections_router.get("", response_model=list[InspectionResponse])
def get_inspections(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get all inspections."""
    return InspectionService.get_inspections(db, skip=skip, limit=limit)


@inspections_router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection(
    inspection_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific inspection by ID."""
    inspection = InspectionService.get_inspection(db, inspection_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return inspection


@inspections_router.post("/{inspection_id}/process")
def process_inspection(
    inspection_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Manually trigger processing of an inspection."""
    inspection = InspectionService.get_inspection(db, inspection_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    
    if inspection.status == "completed":
        raise HTTPException(status_code=400, detail="Inspection already processed. View results in Pothole Map and Maintenance Tickets.")
    
    if inspection.status == "processing":
        raise HTTPException(status_code=400, detail="Inspection is currently being processed. Please wait for completion.")
    
    # Start background processing
    output_dir = os.path.join("backend/detections", str(inspection.id))
    os.makedirs(output_dir, exist_ok=True)
    
    background_tasks.add_task(
        process_inspection_background,
        inspection.id,
        inspection.file_path,
        output_dir,
        db,
        inspection.road_name,
        inspection.area
    )
    
    return {"message": "Processing started", "inspection_id": inspection_id}


@inspections_router.patch("/{inspection_id}", response_model=InspectionResponse)
def update_inspection(
    inspection_id: int,
    update_data: InspectionUpdate,
    db: Session = Depends(get_db)
):
    """Update an inspection."""
    inspection = InspectionService.update_inspection(db, inspection_id, update_data)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return inspection


@inspections_router.delete("/{inspection_id}")
def delete_inspection(
    inspection_id: int,
    db: Session = Depends(get_db)
):
    """Delete an inspection."""
    success = InspectionService.delete_inspection(db, inspection_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return {"message": "Inspection deleted successfully"}
