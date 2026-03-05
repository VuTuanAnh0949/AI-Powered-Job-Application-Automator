"""Shared type definitions and constants."""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class ApplicationStatus(str, Enum):
    """Application status enum."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class JobType(str, Enum):
    """Job type enum."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class WorkArrangement(str, Enum):
    """Work arrangement enum."""
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class JobSearchRequest(BaseModel):
    """Job search request model."""
    keywords: List[str]
    location: str = "Remote"
    job_site: str = "linkedin"
    max_results: int = Field(default=50, ge=1, le=200)
    experience_level: Optional[str] = None


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
    match_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class Experience(BaseModel):
    """Work experience model."""
    company: str
    title: str
    start_date: str
    end_date: Optional[str] = None
    description: str
    achievements: List[str] = []


class Education(BaseModel):
    """Education model."""
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: str
    gpa: Optional[float] = None


class UserProfile(BaseModel):
    """User profile model."""
    id: Optional[str] = None
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    
    summary: Optional[str] = None
    skills: List[str] = []
    experience: List[Experience] = []
    education: List[Education] = []
    certifications: List[str] = []
    languages: List[str] = []
