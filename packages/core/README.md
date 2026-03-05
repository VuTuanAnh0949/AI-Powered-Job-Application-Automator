# AutoApply AI Core

Core business logic and services for job search automation.

This package contains the main business logic that will be refactored from the existing codebase.

## Structure (To be implemented)

```
packages/core/
├── job_search/          # Job search services
├── document_generation/ # Resume/cover letter generation
├── application/         # Application management
├── ai/                  # AI/LLM integrations
└── scraping/            # Web scraping utilities
```

## Migration Plan

The following modules from `job_application_automation/src/` will be migrated here:
- Job search logic (LinkedIn, Indeed, Glassdoor integrations)
- Resume and cover letter generation
- Application tracking
- AI provider integrations
- Database models and operations

## Usage

```python
from packages.core.job_search import JobSearchService
from packages.core.document_generation import ResumeGenerator

# Use core services
search_service = JobSearchService()
jobs = await search_service.search(keywords=["Python Developer"])

generator = ResumeGenerator()
resume = generator.generate(job_description, profile)
```
