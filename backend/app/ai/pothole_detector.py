from pathlib import Path
from typing import List, Dict, Optional

import cv2
from app.config import settings


class PotholeDetector:
    """Run pothole inference with an Ultralytics YOLO weights file."""

    def __init__(self, model_path: Optional[str] = None, demo_mode: Optional[bool] = None):
        self.model_path = Path(model_path or settings.AI_MODEL_PATH)
        if not self.model_path.is_absolute():
            backend_root = Path(__file__).resolve().parents[2]
            self.model_path = backend_root / self.model_path
        self.demo_mode = settings.DEMO_MODE if demo_mode is None else demo_mode
        self.model = None
        self.confidence_threshold = settings.CONFIDENCE_THRESHOLD

        if not self.demo_mode:
            if not self.load_model():
                raise RuntimeError(
                    f"Real AI mode is enabled, but model weights were not found or could not be loaded: {self.model_path}. "
                    "Add a trained pothole YOLO .pt file or set AI_MODEL_PATH in backend/.env."
                )

    def load_model(self) -> bool:
        """Load the configured YOLO weights. Never silently switch to fake detections."""
        if not self.model_path.is_file():
            raise FileNotFoundError(f"YOLO model weights not found: {self.model_path}")
        try:
            from ultralytics import YOLO
            self.model = YOLO(str(self.model_path))
            return True
        except Exception as exc:
            raise RuntimeError(f"Could not load YOLO model at {self.model_path}: {exc}") from exc

    def detect_frame(self, frame_path: str) -> List[Dict]:
        """Detect potholes in one extracted video frame."""
        frame = cv2.imread(frame_path)
        if frame is None:
            return []

        if self.demo_mode:
            return self._demo_detection(frame)

        if self.model is None:
            raise RuntimeError("YOLO model is not loaded; real inference cannot run.")

        results = self.model.predict(
            source=frame,
            conf=self.confidence_threshold,
            verbose=False
        )
        detections = []
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0]) if box.cls is not None else 0
                class_name = str(result.names.get(class_id, class_id)).lower()
                # The configured weights should be trained for pothole detection.
                if confidence >= self.confidence_threshold:
                    detections.append({
                        "bbox": [float(x1), float(y1), float(x2), float(y2)],
                        "confidence": confidence,
                        "class": class_name,
                        "class_id": class_id,
                        "demo": False
                    })
        return detections

    def _demo_detection(self, frame) -> List[Dict]:
        """Generate clearly marked sample detections for demonstration only."""
        import random

        height, width = frame.shape[:2]
        if width < 100 or height < 100:
            return []
        detections = []
        for _ in range(random.randint(0, 2)):
            x1 = random.randint(0, max(0, width - 80))
            y1 = random.randint(height // 2, max(height // 2, height - 50))
            x2 = min(width, x1 + random.randint(30, 80))
            y2 = min(height, y1 + random.randint(20, 50))
            detections.append({
                "bbox": [x1, y1, x2, y2],
                "confidence": round(random.uniform(0.60, 0.95), 4),
                "class": "pothole",
                "demo": True
            })
        return detections

    def detect_batch(self, frame_paths: List[str]) -> Dict[str, List[Dict]]:
        """Run detection for each frame and preserve its source path."""
        return {frame_path: self.detect_frame(frame_path) for frame_path in frame_paths}
