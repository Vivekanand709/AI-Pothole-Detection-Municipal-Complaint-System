from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Pothole(Base):
    __tablename__ = "potholes"
    
    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    timestamp = Column(Float, nullable=False)  # Timestamp in video (seconds)
    frame_number = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    confidence = Column(Float, nullable=False)
    severity = Column(String, nullable=False)  # Low, Medium, High, Critical
    image_path = Column(String, nullable=True)
    bbox = Column(String, nullable=False)  # JSON string of bounding box [x1, y1, x2, y2]
    status = Column(String, default="detected")  # detected, reported, resolved
    road_name = Column(String, nullable=True)
    area = Column(String, nullable=True)
    state = Column(String, nullable=True)  # Indian state
    district = Column(String, nullable=True)  # Indian district
    city = Column(String, nullable=True)  # Indian city
    ward = Column(String, nullable=True)  # Municipal ward
    zone = Column(String, nullable=True)  # Municipal zone
    detection_metadata = Column(Text, nullable=True)  # Additional metadata as JSON
    
    # Relationships
    inspection = relationship("Inspection", back_populates="potholes")
    maintenance_ticket = relationship("MaintenanceTicket", back_populates="pothole", uselist=False)
