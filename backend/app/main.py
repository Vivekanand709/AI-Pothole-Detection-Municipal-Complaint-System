from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings
from app.api import auth_router, inspections_router, potholes_router, tickets_router, dashboard_router, citizen_reports_router
from app.models import User, Inspection, Pothole, MaintenanceTicket, CitizenReport

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Municipal Road Monitoring API",
    description="AI-based road monitoring and pothole management platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(inspections_router)
app.include_router(potholes_router)
app.include_router(tickets_router)
app.include_router(dashboard_router)
app.include_router(citizen_reports_router)

# Serve citizen-uploaded report photos
from fastapi.staticfiles import StaticFiles
from pathlib import Path
citizen_uploads = Path(__file__).resolve().parents[1] / "uploads" / "citizen_reports"
citizen_uploads.mkdir(parents=True, exist_ok=True)
app.mount("/uploads/citizen_reports", StaticFiles(directory=str(citizen_uploads)), name="citizen-report-uploads")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Municipal Road Monitoring API",
        "version": "1.0.0",
        "demo_mode": settings.DEMO_MODE,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Create default admin user on startup
@app.on_event("startup")
async def startup_event():
    """Create default admin user if not exists."""
    from app.database import SessionLocal
    from app.services.auth_service import AuthService
    
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin = AuthService.get_user_by_email(db, "admin@municipal.gov")
        if not admin:
            # Create default admin user
            admin = AuthService.create_user(
                db,
                name="System Administrator",
                email="admin@municipal.gov",
                password="admin123",  # Change this in production!
                role="Admin"
            )
            print("Default admin user created: admin@municipal.gov / admin123")
        
        # Create demo users if they don't exist
        demo_officer = AuthService.get_user_by_email(db, "officer@municipal.gov")
        if not demo_officer:
            AuthService.create_user(
                db,
                name="Demo Officer",
                email="officer@municipal.gov",
                password="officer123",
                role="Municipal Officer"
            )
            print("Demo officer user created: officer@municipal.gov / officer123")
        
        demo_inspector = AuthService.get_user_by_email(db, "inspector@municipal.gov")
        if not demo_inspector:
            AuthService.create_user(
                db,
                name="Demo Inspector",
                email="inspector@municipal.gov",
                password="inspector123",
                role="Inspector"
            )
            print("Demo inspector user created: inspector@municipal.gov / inspector123")
            
    except Exception as e:
        print(f"Error creating default users: {e}")
        print("Continuing with application startup...")
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
