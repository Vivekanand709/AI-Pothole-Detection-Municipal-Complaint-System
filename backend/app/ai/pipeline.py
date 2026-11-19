import os
import json
from typing import List, Dict, Optional, Callable
from pathlib import Path

from app.ai.video_processor import VideoProcessor
from app.ai.pothole_detector import PotholeDetector
from app.ai.severity_classifier import SeverityClassifier
from app.ai.gps_processor import GPSProcessor
from app.ai.ticket_generator import TicketGenerator
from app.config import settings


class Pipeline:
    """Main pipeline for processing road inspection videos."""
    
    def __init__(
        self,
        video_path: str,
        output_dir: str,
        demo_mode: Optional[bool] = None,
        progress_callback: Optional[Callable] = None
    ):
        self.video_path = video_path
        self.output_dir = output_dir
        self.demo_mode = settings.DEMO_MODE if demo_mode is None else demo_mode
        self.progress_callback = progress_callback
        
        # Initialize components
        self.video_processor = VideoProcessor(video_path, output_dir)
        self.pothole_detector = PotholeDetector(demo_mode=self.demo_mode)
        self.severity_classifier = SeverityClassifier()
        self.gps_processor = GPSProcessor()
        self.ticket_generator = TicketGenerator()
        
        # Results storage
        self.detections = []
        self.processed_frames = 0
        self.total_frames = 0
    
    def _update_progress(self, progress: float, message: str = ""):
        """Update progress if callback is provided."""
        if self.progress_callback:
            self.progress_callback(progress, message)
    
    def process(
        self,
        frame_interval: int = 30,
        gps_file_path: Optional[str] = None,
        road_name: Optional[str] = None,
        area: Optional[str] = None
    ) -> Dict:
        """
        Process the complete pipeline.
        
        Args:
            frame_interval: Extract every Nth frame
            gps_file_path: Path to GPS data file (optional)
            road_name: Name of the road being inspected
            area: Area/region name
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Step 1: Validate video
            self._update_progress(5, "Validating video...")
            is_valid, error_msg = self.video_processor.validate_video()
            if not is_valid:
                return {
                    "success": False,
                    "error": error_msg,
                    "detections": []
                }
            
            # Step 2: Get video info
            self._update_progress(10, "Getting video information...")
            video_info = self.video_processor.get_video_info()
            self.total_frames = video_info.get("total_frames", 0)
            duration = video_info.get("duration", 0)
            
            # Step 3: Load GPS data if provided
            gps_source = "uploaded_track"
            if gps_file_path and os.path.exists(gps_file_path):
                self._update_progress(15, "Loading GPS data...")
                if not self.gps_processor.load_gps_from_file(gps_file_path):
                    return {
                        "success": False,
                        "error": "GPS file could not be read. Expected CSV or JSON with timestamp, latitude and longitude.",
                        "detections": []
                    }
            elif self.demo_mode:
                self._update_progress(15, "Generating demo GPS data...")
                self.gps_processor.generate_demo_gps(duration)
                gps_source = "simulated_demo_track"
            else:
                # Real mode must never invent a moving GPS track.
                self._update_progress(15, "No GPS track supplied; using configured fallback coordinates.")
                gps_source = "configured_fallback"
            
            # Step 4: Extract frames
            self._update_progress(20, "Extracting frames...")
            frames_output_dir = os.path.join(self.output_dir, "frames")
            frames = self.video_processor.extract_frames(frame_interval)
            
            if not frames:
                return {
                    "success": False,
                    "error": "No frames extracted from video",
                    "detections": []
                }
            
            # Step 5: Detect potholes in frames
            self._update_progress(40, "Detecting potholes...")
            frame_paths = [frame[2] for frame in frames]
            detection_results = self.pothole_detector.detect_batch(frame_paths)
            
            # Step 6: Process detections
            self._update_progress(60, "Processing detections...")
            all_detections = []
            
            for frame_number, timestamp, frame_path in frames:
                detections = detection_results.get(frame_path, [])
                
                # Ensure detections is a list
                if not isinstance(detections, list):
                    print(f"Warning: detections for {frame_path} is not a list: {type(detections)}")
                    continue
                
                for detection in detections:
                    # Ensure detection is a dictionary
                    if not isinstance(detection, dict):
                        print(f"Warning: detection is not a dict: {type(detection)}")
                        continue
                    
                    # Get GPS coordinates for this timestamp
                    lat, lon = self.gps_processor.get_coordinates_at_timestamp(timestamp)
                    
                    # Classify severity
                    severity, metadata = self.severity_classifier.classify(detection)
                    
                    # Store detection
                    pothole_data = {
                        "frame_number": frame_number,
                        "timestamp": timestamp,
                        "frame_path": frame_path,
                        "bbox": detection["bbox"],
                        "confidence": detection["confidence"],
                        "severity": severity,
                        "latitude": lat,
                        "longitude": lon,
                        "road_name": road_name,
                        "area": area,
                        "state": None,  # Will be set from inspection
                        "district": None,  # Will be set from inspection
                        "city": None,  # Will be set from inspection
                        "ward": None,  # Will be set from inspection
                        "zone": None,  # Will be set from inspection
                        "detection_metadata": json.dumps(metadata),
                        "demo_mode": detection.get("demo", False),
                        "gps_source": gps_source
                    }
                    
                    all_detections.append(pothole_data)
            
            self.detections = all_detections
            self.processed_frames = len(frames)
            
            # Step 7: Generate tickets
            self._update_progress(80, "Generating maintenance tickets...")
            tickets = []
            for detection in all_detections:
                ticket_data = self.ticket_generator.create_ticket_data(detection)
                tickets.append(ticket_data)
            
            # Step 8: Finalize
            self._update_progress(100, "Processing complete!")
            
            return {
                "success": True,
                "detections": all_detections,
                "tickets": tickets,
                "video_info": video_info,
                "total_detections": len(all_detections),
                "demo_mode": self.demo_mode,
                "gps_source": gps_source
            }
            
        except Exception as e:
            print(f"Error in pipeline processing: {e}")
            return {
                "success": False,
                "error": str(e),
                "detections": []
            }
    
    def get_processing_summary(self) -> Dict:
        """Get a summary of the processing results."""
        if not self.detections:
            return {
                "total_detections": 0,
                "severity_breakdown": {},
                "average_confidence": 0.0
            }
        
        severity_counts = {}
        total_confidence = 0.0
        
        for detection in self.detections:
            severity = detection.get("severity", "Unknown")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            total_confidence += detection.get("confidence", 0.0)
        
        return {
            "total_detections": len(self.detections),
            "severity_breakdown": severity_counts,
            "average_confidence": total_confidence / len(self.detections) if self.detections else 0.0,
            "processed_frames": self.processed_frames,
            "total_frames": self.total_frames
        }
