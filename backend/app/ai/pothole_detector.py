import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from app.config import settings


class PotholeDetector:
    """Detect potholes in video frames using YOLO model."""
    
    def __init__(self, model_path: Optional[str] = None, demo_mode: bool = True):
        self.model_path = model_path or settings.AI_MODEL_PATH
        self.demo_mode = demo_mode or settings.DEMO_MODE
        self.model = None
        self.confidence_threshold = settings.CONFIDENCE_THRESHOLD
        
        if not self.demo_mode:
            self.load_model()
    
    def load_model(self) -> bool:
        """Load YOLO model for pothole detection."""
        try:
            from ultralytics import YOLO
            self.model = YOLO(self.model_path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to demo mode")
            self.demo_mode = True
            return False
    
    def detect_frame(self, frame_path: str) -> List[Dict]:
        """
        Detect potholes in a single frame.
        
        Args:
            frame_path: Path to the frame image
            
        Returns:
            List of detection dictionaries with bbox, confidence, etc.
        """
        if self.demo_mode:
            return self._demo_detection(frame_path)
        
        if not self.model:
            self.demo_mode = True
            return self._demo_detection(frame_path)
        
        try:
            # Read frame
            frame = cv2.imread(frame_path)
            if frame is None:
                return []
            
            # Run inference
            results = self.model(frame, conf=self.confidence_threshold)
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    confidence = float(box.conf[0])
                    
                    if confidence >= self.confidence_threshold:
                        detections.append({
                            "bbox": [x1, y1, x2, y2],
                            "confidence": confidence,
                            "class": "pothole"
                        })
            
            return detections
            
        except Exception as e:
            print(f"Error in detection: {e}")
            return []
    
    def _demo_detection(self, frame_path: str) -> List[Dict]:
        """
        Generate demo detections for testing without actual model.
        This creates realistic-looking mock detections.
        """
        try:
            frame = cv2.imread(frame_path)
            if frame is None:
                return []
            
            height, width = frame.shape[:2]
            
            # Generate 1-3 random detections per frame
            import random
            num_detections = random.randint(0, 3)
            
            detections = []
            for _ in range(num_detections):
                # Random position in lower half of frame (where road typically is)
                x1 = random.randint(0, width - 100)
                y1 = random.randint(height // 2, height - 50)
                x2 = x1 + random.randint(30, 100)
                y2 = y1 + random.randint(20, 60)
                
                # Ensure within bounds
                x2 = min(x2, width)
                y2 = min(y2, height)
                
                confidence = random.uniform(0.6, 0.95)
                
                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": confidence,
                    "class": "pothole",
                    "demo": True
                })
            
            return detections
            
        except Exception as e:
            print(f"Error in demo detection: {e}")
            return []
    
    def detect_batch(self, frame_paths: List[str]) -> Dict[str, List[Dict]]:
        """
        Detect potholes in multiple frames.
        
        Args:
            frame_paths: List of frame image paths
            
        Returns:
            Dictionary mapping frame paths to detection lists
        """
        results = {}
        for frame_path in frame_paths:
            results[frame_path] = self.detect_frame(frame_path)
        return results
