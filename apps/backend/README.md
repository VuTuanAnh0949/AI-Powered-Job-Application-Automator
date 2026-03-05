# AutoApply AI Backend

FastAPI-based REST API for AutoApply AI job application automation platform.

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip or uv

### Installation

```bash
# Using pip
pip install -r requirements.txt

# Using uv (recommended)
uv pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Run Development Server

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m app.main
```

The API will be available at:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 📁 Project Structure

```
apps/backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── core/                # Core configuration
│   │   ├── config.py        # Settings & environment
│   │   └── logging.py       # Logging setup
│   ├── api/                 # API layer
│   │   └── v1/
│   │       ├── router.py    # Main API router
│   │       └── endpoints/   # API endpoints
│   │           ├── jobs.py          # Job search endpoints
│   │           ├── applications.py  # Application management
│   │           ├── documents.py     # Document generation
│   │           └── profile.py       # User profile
│   ├── services/            # Business logic services
│   ├── models/              # Database models
│   └── schemas/             # Pydantic schemas
├── tests/                   # Test suite
├── requirements.txt
└── README.md
```

## 🔌 API Endpoints

### Health Check

- `GET /health` - Health check endpoint

### Jobs (`/api/v1/jobs`)

- `POST /search` - Search for jobs across platforms
- `GET /{job_id}` - Get job details
- `POST /{job_id}/analyze` - Analyze job match score

### Applications (`/api/v1/applications`)

- `GET /` - List all applications
- `POST /` - Create new application
- `GET /{id}` - Get application details
- `PATCH /{id}/status` - Update application status
- `DELETE /{id}` - Delete application
- `GET /stats/summary` - Get application statistics

### Documents (`/api/v1/documents`)

- `POST /resume/generate` - Generate tailored resume
- `POST /cover-letter/generate` - Generate cover letter
- `POST /resume/upload` - Upload base resume
- `GET /{id}/download` - Download document
- `GET /{id}/preview` - Preview document

### Profile (`/api/v1/profile`)

- `GET /` - Get user profile
- `POST /` - Create/update profile
- `PATCH /skills` - Update skills
- `PATCH /preferences` - Update job preferences

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

## 🐳 Docker

```bash
# Build image
docker build -t autoapply-backend .

# Run container
docker run -p 8000:8000 --env-file .env autoapply-backend
```

## 📝 Development

### Code Style

This project follows:

- PEP 8 style guide
- Type hints for all functions
- Docstrings for classes and functions

### Adding New Endpoint

1. Create endpoint file in `app/api/v1/endpoints/`
2. Define Pydantic models for request/response
3. Implement endpoint logic
4. Add router to `app/api/v1/router.py`
5. Write tests in `tests/`

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🔒 Security

- All endpoints should be authenticated (TODO: implement JWT)
- Environment variables for sensitive data
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy
- CORS configuration for allowed origins

## 📖 Documentation

Full API documentation available at `/api/docs` when server is running.

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Add tests
4. Submit pull request

## 📄 License

MIT License - See LICENSE file for details
