"""
Test video upload to the backend API with Indian municipal fields.
"""
import requests
import os

# Backend URL
BASE_URL = "http://localhost:8000"

# Video path
video_path = r"C:\Users\HP\OneDrive\Pictures\Desktop\SIH\municipal-road-monitoring\data\demo\test_inspection.mp4"

# Check if video exists
if not os.path.exists(video_path):
    print(f"Video not found: {video_path}")
    exit(1)

print(f"Testing upload of: {video_path}")

# Prepare upload data
files = {
    'video': open(video_path, 'rb')
}

data = {
    'road_name': 'Grand Trunk Road',
    'area': 'Model Town',
    'state': 'Punjab',
    'district': 'Jalandhar',
    'city': 'Jalandhar',
    'ward': 'Ward 8',
    'zone': 'Zone B',
    'notes': 'Test inspection upload - Jalandhar, Punjab (simulated data)'
}

try:
    # Upload video
    response = requests.post(f"{BASE_URL}/api/inspections/upload", files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
finally:
    files['video'].close()
