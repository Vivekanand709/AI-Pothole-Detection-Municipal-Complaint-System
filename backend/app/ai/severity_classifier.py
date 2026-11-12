import json
from typing import Dict, Tuple
from enum import Enum


class Severity(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class SeverityClassifier:
    """Classify pothole severity based on detection metrics."""
    
    def __init__(self):
        # Severity thresholds (configurable)
        self.area_thresholds = {
            Severity.LOW: 1000,      # pixels squared
            Severity.MEDIUM: 3000,
            Severity.HIGH: 6000,
            Severity.CRITICAL: 10000
        }
        
        self.confidence_weights = {
            Severity.LOW: 0.5,
            Severity.MEDIUM: 0.7,
            Severity.HIGH: 0.85,
            Severity.CRITICAL: 0.9
        }
    
    def calculate_area(self, bbox: list) -> float:
        """Calculate bounding box area in pixels."""
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        return width * height
    
    def classify(self, detection: Dict) -> Tuple[str, Dict]:
        """
        Classify pothole severity based on multiple factors.
        
        Args:
            detection: Detection dictionary with bbox, confidence, etc.
            
        Returns:
            Tuple of (severity_label, classification_metadata)
        """
        bbox = detection.get("bbox", [0, 0, 0, 0])
        confidence = detection.get("confidence", 0.0)
        
        # Calculate area
        area = self.calculate_area(bbox)
        
        # Base severity from area
        severity = self._classify_by_area(area)
        
        # Adjust based on confidence
        severity = self._adjust_by_confidence(severity, confidence)
        
        # Check for demo mode flag
        is_demo = detection.get("demo", False)
        
        metadata = {
            "area": area,
            "confidence": confidence,
            "bbox": bbox,
            "base_severity": severity.value,
            "demo_mode": is_demo,
            "factors": {
                "area_based": self._classify_by_area(area).value,
                "confidence_adjusted": severity.value
            }
        }
        
        return severity.value, metadata
    
    def _classify_by_area(self, area: float) -> Severity:
        """Classify severity based on area alone."""
        if area >= self.area_thresholds[Severity.CRITICAL]:
            return Severity.CRITICAL
        elif area >= self.area_thresholds[Severity.HIGH]:
            return Severity.HIGH
        elif area >= self.area_thresholds[Severity.MEDIUM]:
            return Severity.MEDIUM
        else:
            return Severity.LOW
    
    def _adjust_by_confidence(self, severity: Severity, confidence: float) -> Severity:
        """Adjust severity based on detection confidence."""
        # If confidence is very high, potentially upgrade severity
        if confidence >= 0.95 and severity != Severity.CRITICAL:
            severity_levels = [Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]
            current_index = severity_levels.index(severity)
            if current_index < len(severity_levels) - 1:
                return severity_levels[current_index + 1]
        
        # If confidence is low, potentially downgrade severity
        elif confidence < 0.6 and severity != Severity.LOW:
            severity_levels = [Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]
            current_index = severity_levels.index(severity)
            if current_index > 0:
                return severity_levels[current_index - 1]
        
        return severity
    
    def classify_batch(self, detections: list) -> list:
        """
        Classify severity for multiple detections.
        
        Args:
            detections: List of detection dictionaries
            
        Returns:
            List of tuples (severity, metadata)
        """
        results = []
        for detection in detections:
            severity, metadata = self.classify(detection)
            results.append((severity, metadata))
        return results
