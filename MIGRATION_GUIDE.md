# Migration Guide - AutoApply AI v1 → v2

## Overview

This guide explains how to migrate from the legacy codebase (`job_application_automation/`) to the new monorepo structure (`apps/` & `packages/`).

## Architecture Changes

### Before (v1)
```
job_application_automation/
├── src/
│   ├── main.py
│   ├── cli.py
│   ├── job_sources/
│   ├── resume_cover_letter_generator.py
│   ├── application_tracker.py
│   └── ...
├── config/
├── data/
└── templates/
```

### After (v2)
```
apps/
├── backend/               # FastAPI REST API
│   └── app/
│       ├── api/v1/       # API endpoints
│       └── core/         # Config
└── frontend/             # React UI
    └── src/
        ├── pages/
        └── components/

packages/
├── core/                 # Business logic (migrated here)
│   ├── job_search/
│   ├── document_generation/
│   └── application/
└── shared/               # Common utilities
```

## Migration Status

| Component | Old Location | New Location | Status |
|-----------|-------------|--------------|--------|
| **Job Search** | `src/job_sources/` | `packages/core/job_search/` | 🔄 Pending |
| LinkedIn Integration | `src/job_sources/linkedin_integration.py` | → `packages/core/job_search/linkedin.py` | 🔄 Pending |
| Indeed Integration | `src/job_sources/indeed_integration.py` | → `packages/core/job_search/indeed.py` | 🔄 Pending |
| **Document Generation** | `src/resume_cover_letter_generator.py` | `packages/core/document_generation/` | 🔄 Pending |
| Resume Generator | Same | → `packages/core/document_generation/resume.py` | 🔄 Pending |
| Cover Letter Generator | Same | → `packages/core/document_generation/cover_letter.py` | 🔄 Pending |
| **Application Tracking** | `src/application_tracker.py` | `packages/core/application/` | 🔄 Pending |
| **Database** | `src/database.py` | `packages/core/database/` | 🔄 Pending |
| **Models** | `src/models.py` | `packages/core/models/` | 🔄 Pending |
| **AI Providers** | `src/llm_providers/` | `packages/core/ai/` | 🔄 Pending |
| **Utilities** | `src/utils/` | `packages/shared/utils.py` | ✅ Partial |
| **API** | `src/interfaces/api.py` | `apps/backend/app/api/v1/` | ✅ Complete |
| **UI** | `src/interfaces/ui_app.py` | `apps/frontend/` | ✅ Complete |

## Step-by-Step Migration Plan

### Phase 1: Setup ✅ COMPLETE
- [x] Create monorepo structure
- [x] Setup backend API with FastAPI
- [x] Setup frontend with React + TypeScript
- [x] Setup Docker & docker-compose
- [x] Create shared types and utilities
- [x] Documentation

### Phase 2: Migrate Core Services 🔄 IN PROGRESS

#### 2.1 Job Search Services

**What to migrate:**
- `job_sources/base.py` → Base interfaces
- `job_sources/linkedin_integration.py` → LinkedIn scraping
- `job_sources/indeed_integration.py` → Indeed scraping
- `job_sources/glassdoor_integration.py` → Glassdoor scraping
- `job_sources/job_search_manager.py` → Search orchestration

**New structure:**
```python
packages/core/job_search/
├── __init__.py
├── base.py              # Base job search interface
├── linkedin.py          # LinkedIn integration
├── indeed.py            # Indeed integration
├── glassdoor.py         # Glassdoor integration
└── manager.py           # Search manager/orchestrator
```

**Backend integration:**
```python
# apps/backend/app/api/v1/endpoints/jobs.py
from packages.core.job_search import JobSearchManager

@router.post("/search")
async def search_jobs(request: JobSearchRequest):
    manager = JobSearchManager()
    results = await manager.search(request)
    return results
```

#### 2.2 Document Generation

**What to migrate:**
- `resume_cover_letter_generator.py` → Split into separate modules
- Resume templates → Keep in data/templates/
- AI prompt engineering → Improve and document

**New structure:**
```python
packages/core/document_generation/
├── __init__.py
├── resume.py            # Resume generation
├── cover_letter.py      # Cover letter generation
├── parser.py            # Parse existing documents
├── optimizer.py         # ATS optimization
└── templates/           # Template helpers
```

#### 2.3 Application Tracking

**What to migrate:**
- `application_tracker.py` → Application service
- Database models → SQLAlchemy models
- Status tracking → State machine

**New structure:**
```python
packages/core/application/
├── __init__.py
├── tracker.py           # Application tracking
├── status.py            # Status management
└── analytics.py         # Statistics & insights
```

#### 2.4 AI/LLM Integration

**What to migrate:**
- `llm_providers/gemini_provider.py` → Gemini integration
- Other providers → OpenAI, Groq, etc.

**New structure:**
```python
packages/core/ai/
├── __init__.py
├── base.py              # Base provider interface
├── gemini.py            # Gemini provider
├── openai.py            # OpenAI provider
├── groq.py              # Groq provider
└── prompt_templates.py  # Reusable prompts
```

#### 2.5 Database & Models

**What to migrate:**
- `models.py` → SQLAlchemy models
- `database.py` → Database connection & session
- Alembic migrations → Update for new structure

**New structure:**
```python
packages/core/database/
├── __init__.py
├── connection.py        # DB connection
├── session.py           # Session management
└── models/
    ├── __init__.py
    ├── user.py
    ├── job.py
    ├── application.py
    └── document.py
```

### Phase 3: Backend Service Layer 🔜 TODO

Create service layer in backend to use core packages:

```python
apps/backend/app/services/
├── __init__.py
├── job_service.py       # Job search service
├── application_service.py  # Application service
├── document_service.py  # Document service
└── profile_service.py   # Profile service
```

### Phase 4: Testing & Validation 🔜 TODO

- [ ] Unit tests for core packages
- [ ] Integration tests for backend
- [ ] E2E tests for frontend
- [ ] Performance testing
- [ ] Load testing

### Phase 5: Deployment 🔜 TODO

- [ ] Setup CI/CD pipeline
- [ ] Production environment configuration
- [ ] Monitoring & logging
- [ ] Backup strategy
- [ ] Rollback plan

## Migration Commands

### Setup New Structure

```bash
# Create environment files
make setup-env

# Install dependencies
make install
```

### Run Both Old and New (Parallel Development)

```bash
# Run legacy system
cd job_application_automation
python -m src.main

# Run new system
make dev-backend  # Terminal 1
make dev-frontend # Terminal 2
```

### Testing Migration

```bash
# Test backend
cd apps/backend
pytest

# Test core packages
cd packages/core
pytest
```

## Breaking Changes

### API Changes

**Old (v1):**
```python
from job_application_automation.src.main import JobApplicationAutomation

automation = JobApplicationAutomation()
jobs = automation.search_jobs(keywords=["Python Developer"])
```

**New (v2):**
```python
from packages.core.job_search import JobSearchManager

manager = JobSearchManager()
jobs = await manager.search(keywords=["Python Developer"])
```

### Configuration Changes

**Old:** `job_application_automation/config/config.yaml`  
**New:** `apps/backend/.env` (environment variables)

### Data Storage Changes

**Old:** `job_application_automation/data/`  
**New:** `data/` (root level, shared)

## Backward Compatibility

The legacy code in `job_application_automation/` will remain functional until migration is complete. After migration:

1. Test new system thoroughly
2. Run both systems in parallel for validation
3. Gradually deprecate old endpoints
4. Archive legacy code

## Questions & Support

For migration questions, contact:
- **Email**: vutuananh0949@gmail.com
- **GitHub Issues**: Create an issue with `migration` label

## Timeline

- **Phase 1** (Setup): ✅ Complete (Day 1)
- **Phase 2** (Core Migration): 🔄 In Progress (Week 1-2)
- **Phase 3** (Backend Services): 🔜 Week 2-3
- **Phase 4** (Testing): 🔜 Week 3-4
- **Phase 5** (Deployment): 🔜 Week 4+

---

*Last Updated: March 5, 2026*
