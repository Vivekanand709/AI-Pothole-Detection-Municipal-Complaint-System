from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.database import Base


class CitizenReport(Base):
    __tablename__ = "citizen_reports"

    id = Column(Integer, primary_key=True, index=True)
    complaint_code = Column(String, unique=True, index=True, nullable=False)
    citizen_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    road_name = Column(String, nullable=True)
    area = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    image_path = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Submitted")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
