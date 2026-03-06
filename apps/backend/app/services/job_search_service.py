"""
Job Search Service
Aggregates jobs from LinkedIn, Indeed, Glassdoor
"""
import structlog
from typing import Optional, List
from datetime import datetime, timedelta
from beanie.operators import In, RegEx

from app.models.mongodb_models import JobListing
from app.db.vector_db import vector_db
from app.job_sources.linkedin_integration import LinkedInScraper
from app.job_sources.indeed_integration import IndeedScraper
from app.job_sources.glassdoor_integration import GlassdoorScraper

logger = structlog.get_logger(__name__)


class JobSearchService:
    """Service for searching and managing job listings"""
    
    def __init__(self):
        self.linkedin = LinkedInScraper()
        self.indeed = IndeedScraper()
        self.glassdoor = GlassdoorScraper()
    
    async def search_jobs(
        self,
        keywords: str,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        sources: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[JobListing]:
        """
        Search jobs across multiple sources
        
        Args:
            keywords: Search query (e.g., "Python Developer")
            location: Location filter (e.g., "Ho Chi Minh City")
            job_type: Job type filter (full_time, part_time, contract, remote)
            sources: List of sources to search (linkedin, indeed, glassdoor)
            limit: Maximum number of results
        """
        sources = sources or ["linkedin", "indeed", "glassdoor"]
        all_jobs = []
        
        # Search LinkedIn
        if "linkedin" in sources:
            try:
                linkedin_jobs = await self.linkedin.search(
                    keywords=keywords,
                    location=location,
                    limit=limit
                )
                all_jobs.extend(linkedin_jobs)
                logger.info("linkedin_search_complete", count=len(linkedin_jobs))
            except Exception as e:
                logger.error("linkedin_search_failed", error=str(e))
        
        # Search Indeed
        if "indeed" in sources:
            try:
                indeed_jobs = await self.indeed.search(
                    keywords=keywords,
                    location=location,
                    limit=limit
                )
                all_jobs.extend(indeed_jobs)
                logger.info("indeed_search_complete", count=len(indeed_jobs))
            except Exception as e:
                logger.error("indeed_search_failed", error=str(e))
        
        # Search Glassdoor
        if "glassdoor" in sources:
            try:
                glassdoor_jobs = await self.glassdoor.search(
                    keywords=keywords,
                    location=location,
                    limit=limit
                )
                all_jobs.extend(glassdoor_jobs)
                logger.info("glassdoor_search_complete", count=len(glassdoor_jobs))
            except Exception as e:
                logger.error("glassdoor_search_failed", error=str(e))
        
        # Save to database and vector index
        saved_jobs = []
        for job_data in all_jobs:
            try:
                # Check if job already exists
                existing = await JobListing.find_one(
                    JobListing.source_url == job_data.get("source_url")
                )
                
                if existing:
                    saved_jobs.append(existing)
                    continue
                
                # Create new job
                job = JobListing(**job_data)
                await job.insert()
                
                # Add to vector index for semantic search
                await vector_db.add_job(
                    job_id=str(job.id),
                    title=job.title,
                    description=job.description,
                    company=job.company
                )
                
                saved_jobs.append(job)
                
            except Exception as e:
                logger.error("job_save_failed", error=str(e), job=job_data.get("title"))
        
        logger.info("job_search_complete", total=len(saved_jobs), sources=sources)
        return saved_jobs[:limit]
    
    async def get_job_by_id(self, job_id: str) -> Optional[JobListing]:
        """Get job by ID"""
        return await JobListing.get(job_id)
    
    async def search_by_keywords(
        self,
        keywords: List[str],
        location: Optional[str] = None,
        limit: int = 50
    ) -> List[JobListing]:
        """Search jobs in database by keywords"""
        query = JobListing.find()
        
        if keywords:
            # Search in title or description
            keyword_patterns = [RegEx(kw, "i") for kw in keywords]
            query = query.find(
                {"$or": [
                    {"title": {"$in": keyword_patterns}},
                    {"description": {"$in": keyword_patterns}}
                ]}
            )
        
        if location:
            query = query.find(RegEx(location, "i"))
        
        jobs = await query.limit(limit).to_list()
        return jobs
    
    async def semantic_search(
        self,
        query: str,
        limit: int = 20
    ) -> List[JobListing]:
        """
        Semantic search using vector similarity
        Find jobs similar to the query text
        """
        # Search in vector database
        results = await vector_db.search_similar_jobs(query, limit=limit)
        
        # Get job details from MongoDB
        job_ids = [r["job_id"] for r in results]
        jobs = await JobListing.find(In(JobListing.id, job_ids)).to_list()
        
        # Add match scores
        score_map = {r["job_id"]: r["score"] for r in results}
        for job in jobs:
            job.match_score = score_map.get(str(job.id), 0.0)
        
        # Sort by score
        jobs.sort(key=lambda x: x.match_score or 0, reverse=True)
        
        logger.info("semantic_search_complete", query=query, results=len(jobs))
        return jobs
    
    async def match_jobs_to_resume(
        self,
        resume_text: str,
        limit: int = 20
    ) -> List[JobListing]:
        """
        Find jobs matching a resume using semantic search
        """
        results = await vector_db.search_by_resume(resume_text, limit=limit)
        
        # Get job details
        job_ids = [r["job_id"] for r in results]
        jobs = await JobListing.find(In(JobListing.id, job_ids)).to_list()
        
        # Add match scores
        score_map = {r["job_id"]: r["score"] for r in results}
        for job in jobs:
            job.match_score = score_map.get(str(job.id), 0.0)
        
        jobs.sort(key=lambda x: x.match_score or 0, reverse=True)
        
        logger.info("resume_match_complete", results=len(jobs))
        return jobs
    
    async def get_recent_jobs(self, days: int = 7, limit: int = 50) -> List[JobListing]:
        """Get recently posted jobs"""
        since = datetime.utcnow() - timedelta(days=days)
        jobs = await JobListing.find(
            JobListing.posted_date >= since
        ).sort(-JobListing.posted_date).limit(limit).to_list()
        
        return jobs
    
    async def refresh_job(self, job_id: str) -> Optional[JobListing]:
        """Refresh job details from source"""
        job = await self.get_job_by_id(job_id)
        if not job:
            return None
        
        # Determine source and refresh
        try:
            if "linkedin" in job.source_url:
                updated_data = await self.linkedin.get_job_details(job.source_url)
            elif "indeed" in job.source_url:
                updated_data = await self.indeed.get_job_details(job.source_url)
            elif "glassdoor" in job.source_url:
                updated_data = await self.glassdoor.get_job_details(job.source_url)
            else:
                logger.warning("unknown_job_source", url=job.source_url)
                return job
            
            # Update job
            for key, value in updated_data.items():
                setattr(job, key, value)
            
            await job.save()
            
            # Update vector index
            await vector_db.add_job(
                job_id=str(job.id),
                title=job.title,
                description=job.description,
                company=job.company
            )
            
            logger.info("job_refreshed", job_id=job_id)
            return job
            
        except Exception as e:
            logger.error("job_refresh_failed", job_id=job_id, error=str(e))
            return job
    
    async def delete_job(self, job_id: str) -> bool:
        """Delete job from database and vector index"""
        try:
            job = await self.get_job_by_id(job_id)
            if not job:
                return False
            
            # Delete from vector index
            await vector_db.delete_job(job_id)
            
            # Delete from MongoDB
            await job.delete()
            
            logger.info("job_deleted", job_id=job_id)
            return True
            
        except Exception as e:
            logger.error("job_delete_failed", job_id=job_id, error=str(e))
            return False


# Global service instance
job_search_service = JobSearchService()


async def get_job_search_service() -> JobSearchService:
    """Dependency for getting job search service"""
    return job_search_service
