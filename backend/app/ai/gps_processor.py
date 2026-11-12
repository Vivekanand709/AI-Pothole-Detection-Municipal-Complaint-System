import json
import csv
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from app.config import settings


class GPSProcessor:
    """Process and associate GPS coordinates with pothole detections."""
    
    def __init__(self, default_lat: float = None, default_lon: float = None):
        self.default_lat = default_lat or settings.DEFAULT_LATITUDE
        self.default_lon = default_lon or settings.DEFAULT_LONGITUDE
        self.gps_data = []
    
    def load_gps_from_file(self, file_path: str) -> bool:
        """
        Load GPS data from CSV or JSON file.
        
        Expected CSV format: timestamp, latitude, longitude
        Expected JSON format: [{"timestamp": 0.0, "latitude": 40.7128, "longitude": -74.0060}, ...]
        """
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.gps_data.append({
                            'timestamp': float(row.get('timestamp', 0)),
                            'latitude': float(row.get('latitude', self.default_lat)),
                            'longitude': float(row.get('longitude', self.default_lon))
                        })
            elif file_ext == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.gps_data = data if isinstance(data, list) else [data]
            else:
                return False
            
            # Sort by timestamp
            self.gps_data.sort(key=lambda x: x['timestamp'])
            return True
            
        except Exception as e:
            print(f"Error loading GPS data: {e}")
            return False
    
    def add_gps_point(self, timestamp: float, latitude: float, longitude: float):
        """Add a single GPS point."""
        self.gps_data.append({
            'timestamp': timestamp,
            'latitude': latitude,
            'longitude': longitude
        })
        self.gps_data.sort(key=lambda x: x['timestamp'])
    
    def get_coordinates_at_timestamp(self, timestamp: float) -> Tuple[float, float]:
        """
        Get GPS coordinates at a specific timestamp with interpolation.
        
        Args:
            timestamp: Video timestamp in seconds
            
        Returns:
            Tuple of (latitude, longitude)
        """
        if not self.gps_data:
            return self.default_lat, self.default_lon
        
        # If timestamp is before first point
        if timestamp <= self.gps_data[0]['timestamp']:
            return self.gps_data[0]['latitude'], self.gps_data[0]['longitude']
        
        # If timestamp is after last point
        if timestamp >= self.gps_data[-1]['timestamp']:
            return self.gps_data[-1]['latitude'], self.gps_data[-1]['longitude']
        
        # Find surrounding points for interpolation
        for i in range(len(self.gps_data) - 1):
            if self.gps_data[i]['timestamp'] <= timestamp <= self.gps_data[i + 1]['timestamp']:
                return self._interpolate(
                    self.gps_data[i],
                    self.gps_data[i + 1],
                    timestamp
                )
        
        return self.default_lat, self.default_lon
    
    def _interpolate(self, point1: Dict, point2: Dict, timestamp: float) -> Tuple[float, float]:
        """
        Linear interpolation between two GPS points.
        
        Args:
            point1: First GPS point
            point2: Second GPS point
            timestamp: Target timestamp
            
        Returns:
            Tuple of (latitude, longitude)
        """
        t1, lat1, lon1 = point1['timestamp'], point1['latitude'], point1['longitude']
        t2, lat2, lon2 = point2['timestamp'], point2['latitude'], point2['longitude']
        
        # Avoid division by zero
        if t2 == t1:
            return lat1, lon1
        
        # Calculate interpolation factor
        factor = (timestamp - t1) / (t2 - t1)
        
        # Interpolate coordinates
        lat = lat1 + factor * (lat2 - lat1)
        lon = lon1 + factor * (lon2 - lon1)
        
        return lat, lon
    
    def generate_demo_gps(self, duration: float, num_points: int = 20) -> List[Dict]:
        """
        Generate demo GPS data for testing.
        
        Args:
            duration: Video duration in seconds
            num_points: Number of GPS points to generate
            
        Returns:
            List of GPS data points
        """
        import random
        
        gps_points = []
        start_lat = self.default_lat
        start_lon = self.default_lon
        
        for i in range(num_points):
            timestamp = (i / (num_points - 1)) * duration if num_points > 1 else 0
            
            # Add some random variation to simulate movement
            lat_variation = random.uniform(-0.001, 0.001)
            lon_variation = random.uniform(-0.001, 0.001)
            
            gps_points.append({
                'timestamp': timestamp,
                'latitude': start_lat + lat_variation,
                'longitude': start_lon + lon_variation
            })
        
        self.gps_data = gps_points
        return gps_points
    
    def clear_gps_data(self):
        """Clear loaded GPS data."""
        self.gps_data = []
