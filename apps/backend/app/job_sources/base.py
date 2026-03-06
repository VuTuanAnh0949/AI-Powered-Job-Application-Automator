"""Base class for job source scrapers"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import structlog

logger = structlog.get_logger(__name__)


class JobSource(ABC):
    """Abstract base class for job scrapers"""
    
    def __init__(self):
        self.name = "base"
    
    @abstractmethod
    async def search(
        self,
        keywords: str,
        location: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Search for jobs
        
        Returns list of job dictionaries with fields:
        - title: str
        - company: str
        - location: str
        - description: str
        - source_url: str
        - posted_date: Optional[datetime]
        - salary_range: Optional[str]
        - job_type: Optional[str]
        - skills_required: Optional[List[str]]
        """
        pass
    
    @abstractmethod
    async def get_job_details(self, url: str) -> Dict:
        """Get detailed information about a specific job"""
        pass
