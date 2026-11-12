"""
Script to create demo data for the municipal road monitoring system.
This creates sample inspections, potholes, and tickets for demonstration.
Uses Indian municipal locations (Punjab, Delhi, etc.) for realistic demo data.
"""
import sys
import os
import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal, engine, Base
from app.models import User, Inspection, Pothole, MaintenanceTicket
from app.services.auth_service import AuthService
from app.services.pothole_service import PotholeService
from app.services.ticket_service import TicketService

# Indian municipal locations for demo
INDIAN_LOCATIONS = [
    {
        "city": "Ludhiana",
        "state": "Punjab",
        "district": "Ludhiana",
        "ward": "Ward 12",
        "zone": "Zone A",
        "roads": ["Main Market Road", "Civil Lines Road", "Bus Stand Road", "Industrial Area Road"],
        "areas": ["Civil Lines", "Industrial Area", "Residential Zone", "Commercial Zone"]
    },
    {
        "city": "Jalandhar",
        "state": "Punjab",
        "district": "Jalandhar",
        "ward": "Ward 8",
        "zone": "Zone B",
        "roads": ["Grand Trunk Road", "Model Town Road", "City Center Road"],
        "areas": ["Model Town", "City Center", "Industrial Estate"]
    },
    {
        "city": "Amritsar",
        "state": "Punjab",
        "district": "Amritsar",
        "ward": "Ward 5",
        "zone": "Zone C",
        "roads": ["Hall Road", "Court Road", "Mall Road"],
        "areas": ["Civil Lines", "Old City", "Raja Sansi"]
    },
    {
        "city": "Chandigarh",
        "state": "Chandigarh",
        "district": "Chandigarh",
        "ward": "Ward 15",
        "zone": "Sector 17",
        "roads": ["Madhya Marg", "Uttar Marg", "Jan Marg"],
        "areas": ["Sector 17", "Sector 22", "Sector 35"]
    },
    {
        "city": "New Delhi",
        "state": "Delhi",
        "district": "Central Delhi",
        "ward": "Ward 25",
        "zone": "Zone Central",
        "roads": ["Connaught Place", "India Gate Road", "Rajpath"],
        "areas": ["Connaught Place", "India Gate", "Rajpath"]
    }
]

def create_demo_data():
    """Create demo data for testing with Indian municipal data."""
    db = SessionLocal()
    
    try:
        # Ensure tables exist
        Base.metadata.create_all(bind=engine)
        
        # Get or create admin user
        admin = AuthService.get_user_by_email(db, "admin@municipal.gov")
        if not admin:
            admin = AuthService.create_user(
                db,
                name="System Administrator",
                email="admin@municipal.gov",
                password="admin123",
                role="Admin"
            )
            print("Created admin user")
        
        # Create demo inspections from different Indian cities
        severity_levels = ["Low", "Medium", "High", "Critical"]
        
        # Ludhiana coordinates
        base_lat = 30.9
        base_lon = 75.85
        
        for location_idx, location in enumerate(INDIAN_LOCATIONS[:3]):  # Use first 3 locations
            # Create inspection
            road_name = random.choice(location["roads"])
            area = random.choice(location["areas"])
            
            inspection = Inspection(
                filename=f"inspection_{location['city'].lower()}_{location_idx}.mp4",
                file_path=f"backend/uploads/inspection_{location['city'].lower()}_{location_idx}.mp4",
                upload_date=datetime.now() - timedelta(days=random.randint(1, 5)),
                uploaded_by=admin.id,
                status="completed",
                processing_progress=100.0,
                total_frames=random.randint(200, 600),
                duration=random.uniform(10, 30),
                road_name=road_name,
                area=area,
                state=location["state"],
                district=location["district"],
                city=location["city"],
                ward=location["ward"],
                zone=location["zone"],
                notes=f"Demo inspection - {location['city']}, {location['state']} (simulated data)"
            )
            db.add(inspection)
            db.commit()
            db.refresh(inspection)
            print(f"Created inspection {inspection.id} for {location['city']}")
            
            # Create potholes for this inspection
            num_potholes = random.randint(4, 8)
            for i in range(num_potholes):
                # Generate coordinates near the city
                lat = base_lat + random.uniform(-0.02, 0.02) + (location_idx * 0.01)
                lon = base_lon + random.uniform(-0.02, 0.02) + (location_idx * 0.01)
                severity = random.choice(severity_levels)
                confidence = random.uniform(0.6, 0.95)
                
                pothole = Pothole(
                    inspection_id=inspection.id,
                    timestamp=i * 2.0,
                    frame_number=i * 30,
                    latitude=lat,
                    longitude=lon,
                    confidence=confidence,
                    severity=severity,
                    image_path=f"backend/detections/{inspection.id}/frame_{i*30:06d}.jpg",
                    bbox=f"[{random.randint(100, 500)}, {random.randint(100, 300)}, {random.randint(200, 600)}, {random.randint(200, 400)}]",
                    status="detected",
                    road_name=road_name,
                    area=area,
                    state=location["state"],
                    district=location["district"],
                    city=location["city"],
                    ward=location["ward"],
                    zone=location["zone"],
                    detection_metadata=f'{{"area": {random.randint(1000, 5000)}, "demo": true}}'
                )
                db.add(pothole)
                db.commit()
                db.refresh(pothole)
                print(f"Created pothole {pothole.id} with severity {severity}")
                
                # Create maintenance ticket for each pothole
                ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
                priority = severity
                
                # Assign teams based on severity and location
                if severity in ["High", "Critical"]:
                    assigned_team = f"{location['city']} Emergency Maintenance"
                else:
                    assigned_team = f"{location['city']} Road Maintenance"
                
                ticket = MaintenanceTicket(
                    ticket_id=ticket_id,
                    pothole_id=pothole.id,
                    priority=priority,
                    status=random.choice(["Open", "Assigned", "In Progress", "Resolved"]),
                    description=f"Pothole detected at {road_name}, {area}, {location['city']}. Severity: {severity}. Confidence: {confidence:.2%}. (Demo data - {location['state']})",
                    assigned_team=assigned_team,
                    created_at=datetime.now() - timedelta(hours=random.randint(1, 72)),
                    resolution_notes="Resolved during routine maintenance" if random.random() > 0.6 else None
                )
                
                if ticket.resolution_notes:
                    ticket.status = "Resolved"
                    ticket.resolved_at = datetime.now() - timedelta(hours=random.randint(1, 24))
                
                db.add(ticket)
                db.commit()
                print(f"Created ticket {ticket_id}")
        
        print("\nDemo data created successfully!")
        print(f"Total inspections: {db.query(Inspection).count()}")
        print(f"Total potholes: {db.query(Pothole).count()}")
        print(f"Total tickets: {db.query(MaintenanceTicket).count()}")
        
    except Exception as e:
        print(f"Error creating demo data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_data()
