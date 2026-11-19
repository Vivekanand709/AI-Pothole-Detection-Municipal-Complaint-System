from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./municipal_road_monitoring.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 500 * 1024 * 1024  # 500MB
    ALLOWED_VIDEO_EXTENSIONS: set = {".mp4", ".avi", ".mov", ".mkv"}
    
    # AI Settings
    AI_MODEL_PATH: str = "models/pothole_detector.pt"
    DEMO_MODE: bool = True  # Set false in backend/.env to require real YOLO inference
    CONFIDENCE_THRESHOLD: float = 0.5
    
    # GPS Settings (Punjab, India - Ludhiana coordinates for demo)
    DEFAULT_LATITUDE: float = 30.9
    DEFAULT_LONGITUDE: float = 75.85
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"


settings = Settings()
