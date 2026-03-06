"""
MongoDB Models using Beanie ODM
"""
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    """Application status enum"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    INTERVIEW = "interview"
    OFFERED = "offered"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"


class JobType(str, Enum):
    """Job type enum"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    REMOTE = "remote"


# ============================================
# User Models
# ============================================

class UserProfile(Document):
    """User profile stored in MongoDB"""
    
    email: Indexed(EmailStr, unique=True)
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    
    # Professional info
    title: Optional[str] = None  # e.g., "Senior Software Engineer"
    summary: Optional[str] = None
    years_of_experience: Optional[int] = None
    
    # Job preferences
    target_roles: List[str] = Field(default_factory=list)
    target_locations: List[str] = Field(default_factory=list)
    
    # Skills and preferences
    skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    preferred_job_types: List[JobType] = Field(default_factory=list)
    preferred_locations: List[str] = Field(default_factory=list)
    target_salary_min: Optional[int] = None
    target_salary_max: Optional[int] = None
    
    # Resume
    resume_url: Optional[str] = None
    resume_text: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        indexes = ["email"]


class Experience(Document):
    """Work experience"""
    
    user_email: Indexed(str)
    
    company: str
    title: str
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_current: bool = False
    
    description: Optional[str] = None
    achievements: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "experiences"
        indexes = ["user_email"]


class Education(Document):
    """Education history"""
    
    user_email: Indexed(str)
    
    institution: str
    degree: str  # e.g., "Bachelor of Science"
    field_of_study: str  # e.g., "Computer Science"
    start_date: datetime
    end_date: Optional[datetime] = None
    gpa: Optional[float] = None
    
    achievements: List[str] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "education"
        indexes = ["user_email"]


# ============================================
# Job Models
# ============================================

class JobListing(Document):
    """Job listing from various sources"""
    
    # Basic info
    title: Indexed(str)
    company: Indexed(str)
    location: str
    job_type: JobType
    
    # Details
    description: str
    requirements: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    
    # Compensation
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "USD"
    
    # Source
    source: str  # linkedin, indeed, glassdoor, etc.
    source_url: str
    source_id: Optional[str] = None
    
    # Additional info
    posted_date: Optional[datetime] = None
    expires_date: Optional[datetime] = None
    remote_ok: bool = False
    skills_required: List[str] = Field(default_factory=list)
    
    # Matching score (calculated)
    match_score: Optional[float] = None
    match_reasons: List[str] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "job_listings"
        indexes = ["title", "company", "source", "created_at"]


# ============================================
# Application Models
# ============================================

class Application(Document):
    """Job application tracking"""
    
    user_email: Indexed(str)
    job_id: Indexed(str)  # Reference to JobListing
    
    # Application details
    status: ApplicationStatus = ApplicationStatus.DRAFT
    applied_date: Optional[datetime] = None
    
    # Documents
    resume_version: Optional[str] = None
    cover_letter: Optional[str] = None
    custom_resume_url: Optional[str] = None
    cover_letter_url: Optional[str] = None
    
    # Tracking
    interview_dates: List[datetime] = Field(default_factory=list)
    follow_up_dates: List[datetime] = Field(default_factory=list)
    notes: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Contact
    recruiter_name: Optional[str] = None
    recruiter_email: Optional[str] = None
    recruiter_phone: Optional[str] = None
    
    # Outcome
    offer_amount: Optional[int] = None
    rejection_reason: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "applications"
        indexes = ["user_email", "job_id", "status", "applied_date"]


# ============================================
# Document Generation Models
# ============================================

class GeneratedDocument(Document):
    """Generated resume or cover letter"""
    
    user_email: Indexed(str)
    job_id: Optional[str] = None
    
    document_type: str  # resume, cover_letter
    version: int = 1
    
    # Content
    content_text: str
    content_markdown: Optional[str] = None
    file_url: Optional[str] = None
    file_format: str = "docx"  # docx, pdf, txt
    
    # Generation details
    ai_provider: str  # gemini, openai, groq
    prompt_used: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "generated_documents"
        indexes = ["user_email", "document_type", "job_id"]


# ============================================
# ATS Analysis Models
# ============================================

class ATSAnalysis(Document):
    """ATS score and analysis for resume-job match"""
    
    user_email: Indexed(str)
    job_id: Indexed(str)
    resume_version: Optional[str] = None
    
    # Scores
    overall_score: float  # 0-100
    keyword_match_score: float
    experience_match_score: float
    skills_match_score: float
    
    # Analysis
    matched_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    
    # Recommendations
    recommendations: List[str] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "ats_analyses"
        indexes = ["user_email", "job_id", "overall_score"]


# List of all document models for Beanie initialization
DOCUMENT_MODELS = [
    UserProfile,
    Experience,
    Education,
    JobListing,
    Application,
    GeneratedDocument,
    ATSAnalysis,
]
