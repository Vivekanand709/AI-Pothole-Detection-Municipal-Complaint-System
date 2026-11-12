import uuid
from typing import Dict, Optional
from datetime import datetime


class TicketGenerator:
    """Generate maintenance tickets for detected potholes."""
    
    def __init__(self):
        self.ticket_counter = 1000
    
    def generate_ticket_id(self) -> str:
        """Generate a unique ticket ID using UUID."""
        import uuid
        return f"TKT-{uuid.uuid4().hex[:8].upper()}"
    
    def determine_priority(self, severity: str) -> str:
        """
        Determine ticket priority based on pothole severity.
        
        Args:
            severity: Pothole severity (Low, Medium, High, Critical)
            
        Returns:
            Priority level (Low, Medium, High, Critical)
        """
        # Priority generally matches severity
        severity_priority_map = {
            "Low": "Low",
            "Medium": "Medium",
            "High": "High",
            "Critical": "Critical"
        }
        return severity_priority_map.get(severity, "Medium")
    
    def generate_description(self, pothole_data: Dict) -> str:
        """
        Generate a description for the maintenance ticket.
        
        Args:
            pothole_data: Dictionary containing pothole information
            
        Returns:
            Description string
        """
        severity = pothole_data.get('severity', 'Unknown')
        confidence = pothole_data.get('confidence', 0.0)
        location = pothole_data.get('road_name', 'Unknown location')
        area = pothole_data.get('area', 'Unknown area')
        
        description = (
            f"Pothole detected at {location}, {area}. "
            f"Severity: {severity}. "
            f"Detection confidence: {confidence:.2%}. "
            f"Automatically generated from road inspection video."
        )
        
        # Add metadata if available
        metadata = pothole_data.get('detection_metadata', {})
        if metadata:
            # Handle if metadata is a JSON string
            if isinstance(metadata, str):
                try:
                    import json
                    metadata = json.loads(metadata)
                except:
                    metadata = {}
            
            area_pixels = metadata.get('area', 0)
            if area_pixels > 0:
                description += f" Estimated area: {area_pixels:.0f} pixels."
        
        return description
    
    def create_ticket_data(self, pothole_data: Dict) -> Dict:
        """
        Create complete ticket data for a pothole.
        
        Args:
            pothole_data: Dictionary containing pothole information
            
        Returns:
            Dictionary with all ticket fields
        """
        severity = pothole_data.get('severity', 'Medium')
        
        ticket_data = {
            'ticket_id': self.generate_ticket_id(),
            'pothole_id': pothole_data.get('id'),
            'priority': self.determine_priority(severity),
            'status': 'Open',
            'description': self.generate_description(pothole_data),
            'assigned_team': None,
            'created_at': datetime.now(),
            'resolution_notes': None,
            'resolved_at': None,
            'resolved_by': None
        }
        
        return ticket_data
    
    def suggest_team(self, severity: str, area: str) -> Optional[str]:
        """
        Suggest an appropriate maintenance team based on severity and area.
        
        Args:
            severity: Pothole severity
            area: Geographic area
            
        Returns:
            Suggested team name or None
        """
        # Simple logic - can be enhanced based on actual municipal structure
        if severity == "Critical":
            return "Emergency Road Crew"
        elif severity == "High":
            return "Priority Maintenance Team"
        elif severity == "Medium":
            return f"{area} Maintenance Team" if area else "General Maintenance"
        else:
            return "Scheduled Maintenance Team"
