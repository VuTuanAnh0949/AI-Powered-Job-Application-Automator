"""Job search and management endpoints."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
import structlog

from app.services.job_search_service import JobSearchService, get_job_search_service
from app.services.ats_service import ATSService, get_ats_service
from app.models.mongodb_models import JobListing as JobModel, UserProfile

logger = structlog.get_logger()
router = APIRouter()


class JobSearchRequest(BaseModel):
    """Job search request model."""
    keywords: str = Field(..., description="Search keywords (e.g., 'Python Developer', 'Data Scientist')")
    location: Optional[str] = Field(default="Remote", description="Job location")
    sources: List[str] = Field(default=["linkedin", "indeed"], description="Job sites to search")
    job_type: Optional[str] = Field(default=None, description="Job type: full_time, part_time, contract, remote")
    limit: int = Field(default=50, ge=1, le=200, description="Maximum number of results")


class JobListing(BaseModel):
    """Job listing model."""
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    posted_date: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = None
    match_score: Optional[float] = None


class JobSearchResponse(BaseModel):
    """Job search response model."""
    total: int
    jobs: List[JobListing]
    search_params: JobSearchRequest


@router.post("/search", response_model=JobSearchResponse)
async def search_jobs(
    request: JobSearchRequest,
    job_service: JobSearchService = Depends(get_job_search_service)
):
    """
    Search for jobs across multiple platforms.
    
    This endpoint performs intelligent job search with:
    - Multi-platform support (LinkedIn, Indeed, Glassdoor)
    - Smart filtering based on your profile
    - Match scoring to prioritize relevant opportunities
    """
    logger.info("Job search requested", keywords=request.keywords, location=request.location)
    
    try:
        # Search jobs using service
        jobs = await job_service.search_jobs(
            keywords=request.keywords,
            location=request.location,
            job_type=request.job_type,
            sources=request.sources,
            limit=request.limit
        )
        
        # Convert to response format
        job_listings = [
            JobListing(
                id=str(job.id),
                title=job.title,
                company=job.company,
                location=job.location,
                description=job.description[:500] + "..." if len(job.description) > 500 else job.description,
                url=job.source_url,
                posted_date=job.posted_date.isoformat() if job.posted_date else None,
                salary_range=job.salary_range,
                job_type=job.job_type.value if job.job_type else None,
                match_score=job.match_score
            )
            for job in jobs
        ]
        
        return JobSearchResponse(
            total=len(job_listings),
            jobs=job_listings,
            search_params=request
        )
    except Exception as e:
        logger.error("Job search failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")


@router.get("/{job_id}", response_model=JobListing)
async def get_job(
    job_id: str,
    job_service: JobSearchService = Depends(get_job_search_service)
):
    """Get detailed information about a specific job."""
    logger.info("Get job details", job_id=job_id)
    
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobListing(
        id=str(job.id),
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        url=job.source_url,
        posted_date=job.posted_date.isoformat() if job.posted_date else None,
        salary_range=job.salary_range,
        job_type=job.job_type.value if job.job_type else None,
        match_score=job.match_score
    )


@router.post("/{job_id}/analyze")
async def analyze_job(
    job_id: str,
    user_email: str = Query(..., description="User email for profile matching"),
    ats_service: ATSService = Depends(get_ats_service)
):
    """
    Analyze job requirements and calculate ATS match score.
    
    Returns detailed analysis including:
    - Overall match score (0-100)
    - Keyword match analysis
    - Skills match
    - Experience match
    - Actionable recommendations
    """
    logger.info("Analyze job", job_id=job_id, user=user_email)
    
    try:
        # Get analysis
        analysis = await ats_service.get_analysis(user_email, job_id)
        
        return {
            "job_id": str(analysis.job_id),
            "user_email": analysis.user_email,
            "overall_score": analysis.overall_score,
            "keyword_match_score": analysis.keyword_match_score,
            "experience_match_score": analysis.experience_match_score,
            "skills_match_score": analysis.skills_match_score,
            "semantic_similarity_score": analysis.semantic_similarity_score,
            "matched_keywords": analysis.matched_keywords[:20],  # Top 20
            "missing_keywords": analysis.missing_keywords[:20],  # Top 20
            "recommendations": analysis.recommendations,
            "analyzed_at": analysis.created_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Job analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/semantic-search")
async def semantic_search(
    query: str = Query(..., description="Search query or resume text"),
    limit: int = Query(20, ge=1, le=100),
    job_service: JobSearchService = Depends(get_job_search_service)
):
    """
    Semantic job search using vector similarity.
    
    Find jobs that match the meaning/context of your query,
    not just exact keyword matches.
    """
    logger.info("Semantic search", query=query[:100])
    
    try:
        jobs = await job_service.semantic_search(query, limit=limit)
        
        job_listings = [
            JobListing(
                id=str(job.id),
                title=job.title,
                company=job.company,
                location=job.location,
                description=job.description[:500] + "..." if len(job.description) > 500 else job.description,
                url=job.source_url,
                posted_date=job.posted_date.isoformat() if job.posted_date else None,
                salary_range=job.salary_range,
                job_type=job.job_type.value if job.job_type else None,
                match_score=job.match_score
            )
            for job in jobs
        ]
        
        return {
            "total": len(job_listings),
            "jobs": job_listings
        }
    except Exception as e:
        logger.error("Semantic search failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/match-resume")
async def match_resume_to_jobs(
    resume_text: str = Query(..., description="Resume text to match"),
    limit: int = Query(20, ge=1, le=100),
    job_service: JobSearchService = Depends(get_job_search_service)
):
    """
    Find jobs matching your resume using AI.
    
    Uses semantic analysis to find jobs that match your skills and experience,
    ranked by relevance.
    """
    logger.info("Match resume to jobs", resume_length=len(resume_text))
    
    try:
        jobs = await job_service.match_jobs_to_resume(resume_text, limit=limit)
        
        job_listings = [
            JobListing(
                id=str(job.id),
                title=job.title,
                company=job.company,
                location=job.location,
                description=job.description[:500] + "..." if len(job.description) > 500 else job.description,
                url=job.source_url,
                posted_date=job.posted_date.isoformat() if job.posted_date else None,
                salary_range=job.salary_range,
                job_type=job.job_type.value if job.job_type else None,
                match_score=job.match_score
            )
            for job in jobs
        ]
        
        return {
            "total": len(job_listings),
            "jobs": job_listings
        }
    except Exception as e:
        logger.error("Resume matching failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")
