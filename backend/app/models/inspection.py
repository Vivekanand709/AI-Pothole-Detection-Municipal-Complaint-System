from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Inspection(Base):
    __tablename__ = "inspections"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="uploaded")  # uploaded, processing, completed, failed
    processing_progress = Column(Float, default=0.0)
    total_frames = Column(Integer, default=0)
    duration = Column(Float, default=0.0)
    road_name = Column(String, nullable=True)
    area = Column(String, nullable=True)
    state = Column(String, nullable=True)  # Indian state
    district = Column(String, nullable=True)  # Indian district
    city = Column(String, nullable=True)  # Indian city
    ward = Column(String, nullable=True)  # Municipal ward
    zone = Column(String, nullable=True)  # Municipal zone
    notes = Column(String, nullable=True)
    
    # Relationships
    potholes = relationship("Pothole", back_populates="inspection", cascade="all, delete-orphan")
