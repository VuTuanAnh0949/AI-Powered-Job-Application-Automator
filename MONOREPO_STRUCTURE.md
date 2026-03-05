# AutoApply AI - Monorepo Structure

Modern monorepo architecture for AutoApply AI job application automation platform.

## 📁 Project Structure

```
ai-powered-job-application-automator/
├── apps/                           # Applications
│   ├── backend/                    # FastAPI REST API
│   │   ├── app/
│   │   │   ├── api/v1/            # API endpoints
│   │   │   │   └── endpoints/     # Route handlers
│   │   │   ├── core/              # Core config & setup
│   │   │   └── main.py            # Application entry
│   │   ├── requirements.txt
│   │   ├── .env.example
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   └── frontend/                   # React + TypeScript
│       ├── src/
│       │   ├── components/        # Reusable components
│       │   ├── pages/             # Page components
│       │   ├── lib/               # Utilities & API
│       │   └── types/             # TypeScript types
│       ├── package.json
│       ├── vite.config.ts
│       ├── Dockerfile
│       └── README.md
│
├── packages/                       # Shared packages
│   ├── core/                      # Core business logic
│   │   ├── job_search/           # Job search services
│   │   ├── document_generation/  # Resume/cover generation
│   │   ├── application/          # Application tracking
│   │   └── ai/                   # AI/LLM integrations
│   │
│   └── shared/                    # Shared utilities
│       ├── types.py              # Common types
│       └── utils.py              # Common utilities
│
├── job_application_automation/     # Legacy code (to be migrated)
│
├── docs/                          # Documentation
├── data/                          # Data storage
├── docker-compose.yml             # Production compose
├── docker-compose.dev.yml         # Development compose
└── README.md                      # This file

```

## 🚀 Quick Start

### Development Setup

#### Option 1: Local Development

**Backend:**
```bash
cd apps/backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd apps/frontend
npm install
cp .env.example .env
npm run dev
```

#### Option 2: Docker Development

```bash
# Start all services with hot-reload
docker-compose -f docker-compose.dev.yml up

# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
# Frontend: http://localhost:3000 (run locally, not in Docker for HMR)
```

### Production Deployment

```bash
# Copy environment file
cp .env.docker.example .env

# Edit .env with your production credentials
nano .env

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🏗️ Architecture

### Backend (FastAPI)

**Clean Architecture with layers:**
- **API Layer** (`app/api/v1/endpoints/`) - HTTP endpoints
- **Service Layer** (to be added) - Business logic
- **Data Layer** (to be added) - Database operations
- **Core** (`app/core/`) - Configuration & setup

**Key Features:**
- ✅ RESTful API with OpenAPI/Swagger docs
- ✅ Structured logging with structlog
- ✅ CORS middleware configured
- ✅ Health check endpoint
- ✅ Environment-based configuration
- 🔄 Database integration (pending)
- 🔄 Authentication/Authorization (pending)

### Frontend (React + TypeScript)

**Modern React architecture:**
- **Pages** - Route-level components
- **Components** - Reusable UI components
- **Lib** - API client & utilities
- **Types** - TypeScript definitions

**Tech Stack:**
- React 18 with hooks
- TypeScript for type safety
- Vite for fast builds
- TailwindCSS for styling
- TanStack Query for data fetching
- React Router for routing
- Zustand for state management

### Shared Packages

**packages/shared/** - Common utilities and types  
**packages/core/** - Core business logic (to be migrated from legacy)

## 📊 Migration Status

| Component | Status | Notes |
|-----------|--------|-------|
| Backend API Structure | ✅ Complete | Clean architecture ready |
| Frontend UI | ✅ Complete | All pages implemented |
| Shared Types | ✅ Complete | Common types defined |
| Docker Setup | ✅ Complete | Dev & prod compose files |
| Job Search Logic | 🔄 Pending | To migrate from legacy |
| Document Generation | 🔄 Pending | To migrate from legacy |
| Database Models | 🔄 Pending | To migrate from legacy |
| Application Tracking | 🔄 Pending | To migrate from legacy |
| AI Integrations | 🔄 Pending | To migrate from legacy |

## 🔧 Development Workflow

### Adding New API Endpoint

1. Create endpoint in `apps/backend/app/api/v1/endpoints/`
2. Add route to `apps/backend/app/api/v1/router.py`
3. Define request/response models
4. Implement business logic
5. Add corresponding frontend API call

### Adding New Frontend Page

1. Create page component in `apps/frontend/src/pages/`
2. Add route in `apps/frontend/src/App.tsx`
3. Add navigation item in `apps/frontend/src/components/Layout.tsx`
4. Implement UI with TailwindCSS
5. Connect to backend API

## 📦 Package Management

### Backend (Python)

```bash
# Add dependency
cd apps/backend
echo "package-name>=1.0.0" >> requirements.txt
pip install -r requirements.txt
```

### Frontend (Node)

```bash
# Add dependency
cd apps/frontend
npm install package-name
```

## 🧪 Testing

### Backend Tests

```bash
cd apps/backend
pytest
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd apps/frontend
npm run test
```

## 📚 Documentation

- **Backend API**: http://localhost:8000/api/docs (when running)
- **Architecture**: `/docs/ARCHITECTURE.md` (to be created)
- **API Reference**: `/docs/API.md`
- **Migration Guide**: `/docs/MIGRATION.md` (to be created)

## 🔐 Environment Variables

### Backend

See `apps/backend/.env.example` for all available variables.

Key variables:
- `GEMINI_API_KEY` - Google Gemini API
- `OPENAI_API_KEY` - OpenAI API
- `GROQ_API_KEY` - Groq API
- `DATABASE_URL` - Database connection
- `LINKEDIN_EMAIL` - LinkedIn credentials
- `LINKEDIN_PASSWORD` - LinkedIn credentials

### Frontend

See `apps/frontend/.env.example`:
- `VITE_API_URL` - Backend API URL

## 🚧 Next Steps

1. **Migrate Core Logic**
   - Move job search services to `packages/core/`
   - Move document generation to `packages/core/`
   - Move database models to `packages/core/`

2. **Implement Backend Services**
   - Job search service layer
   - Document generation service
   - Application tracking service
   - Database integration

3. **Connect Frontend to Backend**
   - Implement real API calls
   - Add loading states
   - Add error handling
   - Add authentication

4. **Add Authentication**
   - JWT token authentication
   - User registration/login
   - Protected routes

5. **Add Testing**
   - Backend unit tests
   - API integration tests
   - Frontend component tests
   - E2E tests

## 🤝 Contributing

1. Create feature branch from `main`
2. Make changes following project structure
3. Test locally
4. Submit pull request

## 📄 License

MIT License - See LICENSE file for details

---

**Developer**: Vu Tuan Anh  
**Email**: vutuananh0949@gmail.com  
**GitHub**: [VuTuanAnh0949](https://github.com/VuTuanAnh0949)
