from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base


class RepairVerification(Base):
    __tablename__ = "repair_verifications"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("maintenance_tickets.id"), nullable=False, index=True)
    before_image_path = Column(String, nullable=False)
    after_image_path = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
