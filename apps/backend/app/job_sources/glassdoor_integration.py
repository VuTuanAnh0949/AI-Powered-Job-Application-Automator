"""Glassdoor job scraper"""
import structlog
from typing import List, Dict, Optional
from datetime import datetime

from .base import JobSource

logger = structlog.get_logger(__name__)


class GlassdoorScraper(JobSource):
    """Glassdoor job scraper (stub implementation)"""
    
    def __init__(self):
        super().__init__()
        self.name = "glassdoor"
        logger.info("glassdoor_scraper_initialized")
    
    async def search(
        self,
        keywords: str,
        location: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Search Glassdoor jobs
        
        TODO: Implement real scraping using Playwright
        - Build Glassdoor search URL
        - Scrape job listings
        - Parse job cards
        - Extract job details
        """
        logger.warning(
            "glassdoor_scraper_stub_called",
            keywords=keywords,
            location=location,
            message="Returning empty results - real scraping not implemented yet"
        )
        
        # Return empty results for now
        # Real implementation would scrape Glassdoor
        return []
    
    async def get_job_details(self, url: str) -> Dict:
        """
        Get detailed Glassdoor job information
        
        TODO: Implement job detail scraping
        """
        logger.warning("glassdoor_job_details_stub_called", url=url)
        
        return {
            "title": "Unknown",
            "company": "Unknown",
            "location": "Unknown",
            "description": "Job details not available (scraper not implemented)",
            "source_url": url,
            "posted_date": datetime.utcnow(),
            "salary_range": None,
            "job_type": None,
            "skills_required": []
        }
