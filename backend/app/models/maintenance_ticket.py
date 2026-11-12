from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class MaintenanceTicket(Base):
    __tablename__ = "maintenance_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True, nullable=False)
    pothole_id = Column(Integer, ForeignKey("potholes.id"), nullable=False)
    assigned_team = Column(String, nullable=True)
    priority = Column(String, nullable=False)  # Low, Medium, High, Critical
    status = Column(String, default="Open")  # Open, Assigned, In Progress, Resolved, Closed
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    pothole = relationship("Pothole", back_populates="maintenance_ticket")
