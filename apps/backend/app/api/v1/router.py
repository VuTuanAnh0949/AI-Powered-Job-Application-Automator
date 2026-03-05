"""API v1 main router."""

from fastapi import APIRouter

from app.api.v1.endpoints import jobs, applications, documents, profile

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
