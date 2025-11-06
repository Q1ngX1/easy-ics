# Easy ICS 📅

[English](README.md) | [中文](README.zh-CN.md)

Intelligent tool to convert images and text into calendar files

## ✨ Core Features

- 🖼️ **OCR Image Recognition** - Extract calendar information from images
- 📝 **Text Parsing** - Extract events from natural language text
- 📅 **ICS Generation** - Generate standard calendar file format
- 🔄 **Complete Workflow** - Generate calendars from images/text in one click

## 🚀 Quick Start

### Backend Service Setup

```bash
# Navigate to backend directory
cd backend

# Start development server
uvicorn app.main:app --reload

# Access API documentation
# Open browser: http://localhost:8000/docs
```

**Detailed Guide:** 📖 [Backend Startup Guide](./backend/docs/BACKEND_STARTUP.md)

### Frontend Development Server Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Access the app
# Open browser: http://localhost:5173
```

## 📁 Project Structure

```
easy-ics/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── api.py             # API routes
│   │   ├── models/            # Data models
│   │   └── services/          # Business logic
│   ├── tests/                 # Unit tests
│   ├── docs/                  # Documentation
│   ├── pyproject.toml         # Project configuration
│   └── backend_startup.py     # Startup script
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── pages/             # Pages
│   │   ├── components/        # Components
│   │   └── App.jsx            # Main application
│   ├── package.json
│   └── vite.config.js
└── docs/                       # Project documentation
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **Tesseract OCR** - Image recognition
- **Python 3.11+** - Programming language

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **CSS3** - Styling

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Backend Startup Guide](./backend/docs/BACKEND_STARTUP.md) | How to start backend service and use startup script |
| [Backend README](./backend/README.md) | Detailed backend project documentation |
| [ICS Service Documentation](./backend/docs/ICS_SERVICE.md) | Complete ICS file generation and parsing documentation |
| [ICS Quick Reference](./backend/docs/ICS_SERVICE_QUICK_REFERENCE.md) | ICS service common methods quick reference |
| [Frontend README](./frontend/README.md) | Frontend project documentation |

## 🔧 Requirements

### Backend
- Python >= 3.11
- pip or uv package manager
- Tesseract OCR (optional, for image recognition)

### Frontend
- Node.js >= 18
- npm or yarn

## ⚙️ Install Dependencies

### Backend

```bash
cd backend

# Option 1: Using pip
pip install -e .

# Option 2: Using uv
uv sync
```

### Frontend

```bash
cd frontend
npm install
```

## 📡 API Endpoints

After starting the backend service, visit http://localhost:8000/docs to view the complete interactive API documentation.

**Main Endpoints:**
- `GET /api/check_health` - Health check
- `POST /api/upload/img` - Upload image for OCR recognition
- `POST /api/upload/text` - Parse text to extract events
- `POST /api/download_ics` - Generate ICS file

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test class
pytest tests/ics_service_test.py -v

# Generate coverage report
pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test
```

## 🐛 FAQ

**Q: How to start the development environment?**

A: Run the following commands:
```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend && npm run dev
```

**Q: How to test the API?**

A: After starting the backend, visit http://localhost:8000/docs and use Swagger UI to test

**Q: How to install Tesseract?**

A: Refer to the installation guide in [Backend README](./backend/README.md#-install-dependencies)

## 📖 Usage Examples

### Generate ICS File from Text

```python
from app.services.ics_service import ICSService
from app.models.event import Event
from datetime import datetime

# Create event
event = Event(
    title="Project Meeting",
    start_time=datetime(2025, 10, 26, 14, 0),
    end_time=datetime(2025, 10, 26, 15, 0),
    location="Meeting Room A"
)

# Generate ICS
service = ICSService()
ics_content = service.generate_ics([event])

# Save file
with open("calendar.ics", "w") as f:
    f.write(ics_content)
```

### Generate Calendar Using API

```bash
curl -X POST "http://localhost:8000/api/download_ics" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "title": "Project Meeting",
        "start_time": "2025-10-26T14:00:00",
        "end_time": "2025-10-26T15:00:00"
      }
    ]
  }' \
  --output calendar.ics
```

## 🚀 Deployment

### Docker Deployment (Coming Soon)

```bash
docker-compose up
```

### Production Deployment

Backend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend:
```bash
npm run build
# Deploy dist directory to static server
```

## 📝 Development Roadmap

- [x] Project structure setup
- [x] Backend framework initialization
- [x] OCR service implementation
- [x] ICS generation service
- [x] ICS parsing service
- [x] Basic API routes
- [x] Frontend page optimization
- [ ] Text parsing service
- [ ] Complete integration tests
- [ ] Docker deployment configuration
- [ ] Production environment optimization

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License - See LICENSE file for details

## 💬 Contact

- GitHub Issues: [Project Issue Tracking](../../issues)
- Project Homepage: [GitHub](https://github.com/Q1ngX1/easy-ics)

---

**Made with ❤️ by the Easy ICS Team** 