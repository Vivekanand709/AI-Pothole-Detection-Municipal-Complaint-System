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
- **Citizen Complaint Portal**: Public photo-based reporting, optional browser GPS, unique tracking code, and complaint status lookup
- **Repair Evidence**: Before/after image submission on maintenance tickets; successful evidence submission records the repair and resolves the ticket

### Demo Mode and real AI
The default configuration is demo mode. The system includes a demonstration workflow that:
- Uses simulated AI detections for demonstration (not model inference)
- Generates approximate GPS coordinates when no GPS track is supplied
- Creates realistic maintenance tickets
- Populates the dashboard with sample data
- Clearly indicates demo mode in the UI


## Citizen complaint workflow

The public citizen portal is available at `/citizen-report`. A citizen can submit their name, contact number, road details, description, an image (JPG/PNG/WEBP up to 8 MB), and optionally share browser GPS coordinates. The API stores the image and complaint in the database and returns a unique tracking code.

Municipal staff can sign in and open `/citizen-reports` to review reports, search by complaint code/road/area/description, filter by status, inspect the submitted photo, open supplied GPS coordinates in a map, and update the complaint status. Citizens can use their tracking code on the public portal to check progress.

For maintenance tickets, authorised staff can open the ticket's repair-verification page, submit before-and-after photos with notes, and resolve the ticket through the verification API.

### Demo limitations

The default `DEMO_MODE` setting is `true`. In this mode, the video-inspection pipeline uses simulated detections and approximate demo coordinates rather than claiming live model inference or hardware GPS. Citizen GPS is only captured when the citizen explicitly grants browser permission. Run and validate the full workflow in your local environment before presenting it as a production municipal deployment.

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
- Upload before/after repair photos in Ticket Details to save evidence and mark the ticket resolved
- Track ticket lifecycle: Open → Assigned → In Progress → Resolved → Closed

### 7. Citizen Complaint Portal
- Open `/citizen-report` without signing in
- Enter contact details and the road issue description
- Attach a JPG, PNG, or WEBP photo (maximum 8 MB)
- Optionally capture the device GPS location (browser permission required)
- Save the generated `RGA-XXXXXXXXXXXX` tracking code and use it to check report status
- Municipal staff can open **Manage Complaints** after signing in to review photos and update statuses

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

### Demo Mode (Default)

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

- [ ] Integration with real GPS hardware and synchronized GPS tracks during video uploads
- [ ] Production-trained pothole model weights and field validation
- [ ] Mobile app for field inspectors
- [ ] Real-time notifications and SMS updates for citizens
- [ ] Municipal work-order integration and deployment hardening

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

**Important implementation note**: The default configuration uses simulated detections and approximate GPS. Real inference requires a compatible trained Ultralytics YOLO weights file at `backend/models/pothole_detector.pt` and `DEMO_MODE=false`. Real GPS requires a timestamped GPS CSV/JSON track; otherwise the application deliberately labels coordinates as demo estimates. Citizen complaints use real uploaded photos and optional browser GPS. Repair evidence uses the uploaded before/after photos. This repository is a project prototype and still needs local end-to-end testing, model validation, security review, and production deployment configuration.


## Real AI inference setup

The video pipeline supports Ultralytics YOLO inference when a **trained pothole model** is provided. The repository does not bundle model weights. A generic pretrained COCO model is not a substitute for pothole-trained weights.

1. Install backend dependencies from `backend/requirements.txt`.
2. Put your trained `pothole_detector.pt` file in `backend/models/`, or configure `AI_MODEL_PATH` in `backend/.env`.
3. Copy `backend/.env.example` to `backend/.env`.
4. Set `DEMO_MODE=false` only after the correct weights are present.
5. Restart the backend and check `http://127.0.0.1:8000/api/inspections/ai/status`. It reports whether weights are available and whether real AI mode is configured.
6. Upload a short road-inspection video and inspect the generated detections. Validate the model on representative local road footage before relying on its predictions.

When real mode is selected, a missing or invalid weights file now raises a clear error instead of silently generating random demo boxes. Demo mode remains the safe default. GPS remains demo-generated unless a GPS track is supplied to the processing pipeline.


## Train a genuine pothole detection model

This repository does not include trained pothole weights. Follow [AI model training guide](docs/AI_MODEL_TRAINING.md) to obtain a properly licensed YOLO-format pothole dataset, train the detector with `scripts/train_pothole_model.py`, and enable real inference. Demo Mode is simulated and must not be presented as real AI output.
