# AI-Based Municipal Road Monitoring & Pothole Management Platform

A comprehensive municipal road monitoring system that uses AI/computer vision to detect potholes from road inspection videos, automatically creates maintenance tickets, and provides a dashboard for municipal teams to monitor and manage road problems.

## 🚀 Features

### Core Functionality
- **Video Upload**: Upload road inspection videos (MP4, AVI, MOV formats)
- **AI Pothole Detection**: Automated pothole detection using computer vision
- **GPS Association**: Approximate GPS coordinates for detected potholes
- **Severity Classification**: Automatic classification (Low, Medium, High, Critical)
- **Maintenance Tickets**: Automatic ticket generation and management
- **Interactive Map**: Leaflet-based map visualization with filtering
- **Dashboard Analytics**: Comprehensive statistics and charts
- **User Authentication**: Role-based access control (Admin, Municipal Officer, Inspector)

### Demo Mode
The system includes a fully functional demo mode that:
- Uses simulated AI detections for demonstration
- Generates approximate GPS coordinates
- Creates realistic maintenance tickets
- Populates the dashboard with sample data
- Clearly indicates demo mode in the UI

## 🏗️ Architecture

### Technology Stack

**Backend:**
- Python 3.8+
- FastAPI (REST API framework)
- SQLAlchemy (ORM)
- SQLite (Database)
- OpenCV (Video processing)
- Ultralytics YOLO (AI detection - optional)

**Frontend:**
- React 19
- Vite (Build tool)
- Tailwind CSS (Styling)
- React Router (Navigation)
- Leaflet + React-Leaflet (Maps)
- Recharts (Charts)
- Axios (HTTP client)

**AI/ML:**
- OpenCV (Video frame extraction)
- YOLO-based detection (with demo fallback)
- Custom severity classification algorithm
- GPS interpolation system

## 📁 Project Structure

```
municipal-road-monitoring/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration settings
│   │   ├── database.py             # Database connection
│   │   ├── api/                    # API endpoints
│   │   │   ├── auth.py            # Authentication endpoints
│   │   │   ├── inspections.py     # Inspection management
│   │   │   ├── potholes.py        # Pothole endpoints
│   │   │   ├── tickets.py         # Ticket management
│   │   │   └── dashboard.py       # Dashboard statistics
│   │   ├── models/                 # Database models
│   │   │   ├── user.py
│   │   │   ├── inspection.py
│   │   │   ├── pothole.py
│   │   │   └── maintenance_ticket.py
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── services/               # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── inspection_service.py
│   │   │   ├── pothole_service.py
│   │   │   ├── ticket_service.py
│   │   │   └── dashboard_service.py
│   │   └── ai/                     # AI processing pipeline
│   │       ├── video_processor.py
│   │       ├── pothole_detector.py
│   │       ├── severity_classifier.py
│   │       ├── gps_processor.py
│   │       ├── ticket_generator.py
│   │       └── pipeline.py
│   ├── uploads/                    # Uploaded video files
│   ├── detections/                 # Processed frames and results
│   └── requirements.txt            # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/                    # API client functions
│   │   ├── components/             # Reusable components
│   │   ├── context/                # React context (Auth)
│   │   └── pages/                  # Page components
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── demo/                       # Demo data files
├── README.md
└── .gitignore
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd municipal-road-monitoring\backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. (Optional) Create demo data:
```bash
python create_demo_data.py
```

6. Start the backend server:
```bash
python -m uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

API documentation available at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd municipal-road-monitoring\frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (or another port if 5173 is in use)

## 🔐 Default Users

The system automatically creates demo users on first startup:

- **Admin**: `admin@municipal.gov` / `admin123`
- **Municipal Officer**: `officer@municipal.gov` / `officer123`
- **Inspector**: `inspector@municipal.gov` / `inspector123`

**⚠️ Important**: Change these passwords in production!

**Demo Mode Login**: In demo mode, you can use any email and password to access the system.

## 📖 Usage Guide

### 1. Login
- Access the application at the frontend URL
- Use any email and password in demo mode
- Different roles have different access levels

### 2. View Dashboard
- Navigate to "Dashboard" page after login
- View key statistics and metrics
- Interactive charts show trends and distributions
- Monitor system performance and pothole patterns

### 3. Upload Road Inspection
- Navigate to "Upload Inspection" page
- Select a video file (MP4, AVI, MOV)
- Optionally add road name, area, and notes
- Click "Upload & Start Processing"
- Processing happens automatically in the background

### 4. Monitor Processing
- Navigate to "Inspection History" to see processing status
- Progress bar shows processing completion
- Status updates: uploaded → processing → completed

### 5. View Results on Map
- Navigate to "Pothole Map" page
- All detected potholes appear as colored markers
- Color indicates severity (green=Low, yellow=Medium, orange=High, red=Critical)
- Click markers to see details
- Use filters to narrow down results

### 6. Manage Maintenance Tickets
- Navigate to "Maintenance Tickets" page
- Tickets are automatically created for each detected pothole
- View ticket details and update status
- Assign teams and add resolution notes
- Track ticket lifecycle: Open → Assigned → In Progress → Resolved → Closed

## 🗺️ GPS Data

The system supports multiple GPS data sources:

1. **Video Metadata**: GPS embedded in video files (if available)
2. **GPS File Upload**: CSV/JSON file with timestamp, latitude, longitude
3. **Demo Mode**: Simulated GPS coordinates for testing

### GPS File Format

**CSV Format:**
```csv
timestamp,latitude,longitude
0.0,30.9,75.85
5.0,30.901,75.851
10.0,30.902,75.852
```

**JSON Format:**
```json
[
  {"timestamp": 0.0, "latitude": 30.9, "longitude": 75.85},
  {"timestamp": 5.0, "latitude": 30.901, "longitude": 75.851},
  {"timestamp": 10.0, "latitude": 30.902, "longitude": 75.852}
]
```

## 🤖 AI Model Setup

### Demo Mode (Current)

The system currently runs in **Demo Mode** by default:
- Simulates realistic pothole detections
- Generates approximate GPS coordinates
- Creates complete workflow for demonstration
- Clearly labels data as simulated
- **No real AI model required**

### Using Real AI Model (Optional)

To use a real YOLO model for pothole detection:

1. Place your trained model file in `backend/models/pothole_detector.pt`
2. The model must be compatible with Ultralytics YOLO format
3. Update `backend/app/config.py`:
   ```python
   DEMO_MODE = False
   AI_MODEL_PATH = "models/pothole_detector.pt"
   ```
4. **Important**: Real pothole model integration requires compatible trained YOLO weights. Demo Mode is used when real weights are unavailable.

### Demo Mode (Default)

The system runs in demo mode by default, which:
- Simulates realistic pothole detections
- Generates approximate GPS coordinates
- Creates complete workflow for demonstration
- Clearly labels data as simulated

## 📊 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Inspection Endpoints

- `POST /api/inspections/upload` - Upload inspection video
- `GET /api/inspections` - List all inspections
- `GET /api/inspections/{id}` - Get specific inspection
- `POST /api/inspections/{id}/process` - Process inspection
- `PATCH /api/inspections/{id}` - Update inspection
- `DELETE /api/inspections/{id}` - Delete inspection

### Pothole Endpoints

- `GET /api/potholes` - List all potholes
- `GET /api/potholes/map` - Get potholes for map display
- `GET /api/potholes/{id}` - Get specific pothole
- `PATCH /api/potholes/{id}/status` - Update pothole status
- `DELETE /api/potholes/{id}` - Delete pothole

### Ticket Endpoints

- `GET /api/tickets` - List all tickets
- `GET /api/tickets/{id}` - Get specific ticket
- `PATCH /api/tickets/{id}` - Update ticket
- `POST /api/tickets/{id}/assign` - Assign ticket to team
- `POST /api/tickets/{id}/resolve` - Mark ticket as resolved
- `POST /api/tickets/{id}/close` - Close ticket
- `DELETE /api/tickets/{id}` - Delete ticket

### Dashboard Endpoints

- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/recent-activity` - Get recent activity

Complete API documentation available at `http://localhost:8000/docs`

## 🔧 Configuration

### Backend Configuration (`backend/app/config.py`)

```python
# Database
DATABASE_URL = "sqlite:///./municipal_road_monitoring.db"

# Security
SECRET_KEY = "your-secret-key-change-in-production"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# File Upload
MAX_UPLOAD_SIZE = 500 * 1024 * 1024  # 500MB
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

# AI Settings
AI_MODEL_PATH = "models/pothole_detector.pt"
DEMO_MODE = True
CONFIDENCE_THRESHOLD = 0.5

# GPS Settings (Punjab, India - Ludhiana coordinates for demo)
DEFAULT_LATITUDE = 30.9
DEFAULT_LONGITUDE = 75.85

# CORS
CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]
```

## 🧪 Testing

### Running Tests

**Backend Tests:**
```bash
cd backend
pytest tests/
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

### Demo Workflow Test

Test the complete workflow:

1. Login with demo credentials
2. Upload a test video
3. Monitor processing in Inspection History
4. View results on Pothole Map
5. Check auto-generated tickets
6. Update ticket status
7. Verify dashboard statistics

## 🔍 Troubleshooting

### Backend Issues

**Database locked error:**
- Ensure only one backend instance is running
- Check for other processes accessing the database

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**Video processing fails:**
- Verify video format is supported (MP4, AVI, MOV)
- Check file size doesn't exceed 500MB limit
- Ensure uploads directory has write permissions

### Frontend Issues

**CORS errors:**
- Verify backend CORS settings include frontend URL
- Check backend is running on correct port (8000)

**Map not displaying:**
- Ensure Leaflet CSS is imported
- Check internet connection for map tiles
- Verify coordinates are valid

**API connection errors:**
- Confirm backend is running
- Check API_BASE_URL in `src/api/client.js`
- Verify no firewall blocking localhost

### AI Processing Issues

**Demo mode not working:**
- Check DEMO_MODE is True in config
- Verify OpenCV is installed correctly
- Check uploads directory exists

**Real model not loading:**
- Verify model file exists at specified path
- Check model format is compatible with Ultralytics
- Ensure sufficient system resources

## 🚀 Future Improvements

- [ ] Integration with real GPS hardware
- [ ] Support for real-time video streaming
- [ ] Mobile app for field inspectors
- [ ] Advanced analytics and reporting
- [ ] Integration with municipal work order systems
- [ ] Multi-language support
- [ ] Real-time notifications
- [ ] Historical trend analysis
- [ ] Weather data integration
- [ ] Citizen reporting portal

## 📝 License

This project is a demonstration/proof-of-concept for municipal road monitoring. For production use, ensure proper licensing of AI models and compliance with local regulations.

## 🤝 Contributing

This is a demonstration project. For production deployments, consider:

1. Security audit and hardening
2. Performance optimization
3. Scalability planning
4. Disaster recovery planning
5. Compliance with municipal IT standards

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Verify configuration settings
- Check system logs for error details

---

**Note**: This system is currently in demo mode. All AI detections and GPS coordinates are simulated for demonstration purposes. For production use, integrate real AI models and GPS data sources.
