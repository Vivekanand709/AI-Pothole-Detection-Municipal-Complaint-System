import cv2
import os
from typing import List, Tuple, Optional
from pathlib import Path


class VideoProcessor:
    """Process video files and extract frames for pothole detection."""
    
    def __init__(self, video_path: str, output_dir: str):
        self.video_path = video_path
        self.output_dir = output_dir
        self.cap = None
        self.fps = 0
        self.total_frames = 0
        self.duration = 0
        
    def open_video(self) -> bool:
        """Open video file and get basic information."""
        try:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                return False
            
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            
            return True
        except Exception as e:
            print(f"Error opening video: {e}")
            return False
    
    def close_video(self):
        """Close video file."""
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def extract_frames(self, frame_interval: int = 30) -> List[Tuple[int, float, str]]:
        """
        Extract frames from video at specified interval.
        
        Args:
            frame_interval: Extract every Nth frame
            
        Returns:
            List of tuples (frame_number, timestamp, frame_path)
        """
        if not self.cap or not self.cap.isOpened():
            if not self.open_video():
                return []
        
        frames = []
        frame_count = 0
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / self.fps if self.fps > 0 else 0
                    frame_filename = f"frame_{frame_count:06d}.jpg"
                    frame_path = os.path.join(self.output_dir, frame_filename)
                    
                    # Save frame
                    cv2.imwrite(frame_path, frame)
                    frames.append((frame_count, timestamp, frame_path))
                
                frame_count += 1
                
        except Exception as e:
            print(f"Error extracting frames: {e}")
        finally:
            self.close_video()
        
        return frames
    
    def get_video_info(self) -> dict:
        """Get video information."""
        if not self.cap:
            if not self.open_video():
                return {}
        
        info = {
            "fps": self.fps,
            "total_frames": self.total_frames,
            "duration": self.duration,
            "width": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        }
        
        self.close_video()
        return info
    
    def validate_video(self) -> Tuple[bool, Optional[str]]:
        """Validate video file."""
        if not os.path.exists(self.video_path):
            return False, "Video file does not exist"
        
        # Check file extension
        valid_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        if not any(self.video_path.lower().endswith(ext) for ext in valid_extensions):
            return False, "Invalid video format"
        
        # Try to open video
        if not self.open_video():
            return False, "Cannot open video file"
        
        self.close_video()
        return True, None
