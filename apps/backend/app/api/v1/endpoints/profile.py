"""User profile management endpoints."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import structlog

from app.models.mongodb_models import (
    UserProfile as UserProfileModel,
    Experience as ExperienceModel,
    Education as EducationModel
)

logger = structlog.get_logger()
router = APIRouter()


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
    
    job_preferences: Optional[dict] = None


@router.get("/{email}", response_model=UserProfile)
async def get_profile(email: str):
    """
    Get user profile by email.
    
    Your profile is used to:
    - Match you with relevant jobs
    - Generate tailored resumes and cover letters
    - Calculate job match scores
    """
    logger.info("Get profile", email=email)
    
    try:
        profile = await UserProfileModel.find_one(UserProfileModel.email == email)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Get experiences
        experiences = await ExperienceModel.find(ExperienceModel.user_email == email).to_list()
        # Get education
        education = await EducationModel.find(EducationModel.user_email == email).to_list()
        
        return UserProfile(
            id=str(profile.id),
            email=profile.email,
            full_name=profile.full_name,
            phone=profile.phone,
            location=profile.location,
            linkedin_url=profile.linkedin_url,
            github_url=profile.github_url,
            portfolio_url=profile.portfolio_url,
            summary=profile.summary,
            skills=profile.skills,
            certifications=profile.certifications,
            languages=profile.languages,
            experience=[
                Experience(
                    company=exp.company,
                    title=exp.position,
                    start_date=exp.start_date,
                    end_date=exp.end_date,
                    description=exp.description,
                    achievements=exp.achievements
                )
                for exp in experiences
            ],
            education=[
                Education(
                    institution=edu.institution,
                    degree=edu.degree,
                    field_of_study=edu.field_of_study,
                    start_date=edu.start_date,
                    end_date=edu.end_date,
                    gpa=float(edu.gpa) if edu.gpa else None
                )
                for edu in education
            ],
            job_preferences={
                "target_roles": profile.target_roles,
                "target_locations": profile.target_locations,
                "years_of_experience": profile.years_of_experience
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get profile", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(e)}")


@router.post("", response_model=UserProfile)
async def create_profile(profile: UserProfile):
    """
    Create or update user profile.
    
    Keep your profile up-to-date for:
    - Better job matching
    - More accurate AI-generated documents
    - Improved success rate
    """
    logger.info("Create/update profile", email=profile.email)
    
    try:
        # Check if profile exists
        existing_profile = await UserProfileModel.find_one(
            UserProfileModel.email == profile.email
        )
        
        if existing_profile:
            # Update existing profile
            existing_profile.full_name = profile.full_name
            existing_profile.phone = profile.phone
            existing_profile.location = profile.location
            existing_profile.linkedin_url = profile.linkedin_url
            existing_profile.github_url = profile.github_url
            existing_profile.portfolio_url = profile.portfolio_url
            existing_profile.summary = profile.summary
            existing_profile.skills = profile.skills
            existing_profile.certifications = profile.certifications
            existing_profile.languages = profile.languages
            existing_profile.target_roles = profile.job_preferences.get("target_roles", []) if profile.job_preferences else []
            existing_profile.target_locations = profile.job_preferences.get("target_locations", []) if profile.job_preferences else []
            existing_profile.years_of_experience = profile.job_preferences.get("years_of_experience", 0) if profile.job_preferences else 0
            
            await existing_profile.save()
            logger.info("Profile updated", email=profile.email)
            
            return UserProfile(
                id=str(existing_profile.id),
                **profile.dict(exclude={"id"})
            )
        else:
            # Create new profile
            new_profile = UserProfileModel(
                email=profile.email,
                full_name=profile.full_name,
                phone=profile.phone,
                location=profile.location,
                linkedin_url=profile.linkedin_url,
                github_url=profile.github_url,
                portfolio_url=profile.portfolio_url,
                summary=profile.summary,
                skills=profile.skills,
                certifications=profile.certifications,
                languages=profile.languages,
                target_roles=profile.job_preferences.get("target_roles", []) if profile.job_preferences else [],
                target_locations=profile.job_preferences.get("target_locations", []) if profile.job_preferences else [],
                years_of_experience=profile.job_preferences.get("years_of_experience", 0) if profile.job_preferences else 0
            )
            
            await new_profile.insert()
            logger.info("Profile created", email=profile.email)
            
            return UserProfile(
                id=str(new_profile.id),
                **profile.dict(exclude={"id"})
            )
    except Exception as e:
        logger.error("Failed to create/update profile", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create/update profile: {str(e)}")


@router.patch("/skills")
async def update_skills(skills: List[str]):
    """Update skills list."""
    logger.info("Update skills", count=len(skills))
    
    # TODO: Implement skills update
    return {"skills": skills}


@router.patch("/preferences")
async def update_preferences(preferences: dict):
    """
    Update job preferences.
    
    Set your preferences for:
    - Desired job titles
    - Preferred locations
    - Salary expectations
    - Work arrangement (remote/hybrid/onsite)
    - Company size preference
    """
    logger.info("Update preferences")
    
    # TODO: Implement preferences update
    return {"preferences": preferences}


# Experience endpoints
class ExperienceCreate(BaseModel):
    """Create experience request."""
    user_email: EmailStr
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    is_current: bool = False
    description: str
    achievements: List[str] = []
    technologies: List[str] = []


@router.post("/experience")
async def add_experience(data: ExperienceCreate):
    """Add work experience to profile."""
    logger.info("Add experience", email=data.user_email, company=data.company)
    
    try:
        # Check if profile exists
        profile = await UserProfileModel.find_one(UserProfileModel.email == data.user_email)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Create experience
        experience = ExperienceModel(
            user_email=data.user_email,
            company=data.company,
            position=data.position,
            start_date=data.start_date,
            end_date=data.end_date,
            is_current=data.is_current,
            description=data.description,
            achievements=data.achievements,
            technologies=data.technologies
        )
        
        await experience.insert()
        logger.info("Experience added",id=str(experience.id))
        
        return {"id": str(experience.id), "message": "Experience added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to add experience", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to add experience: {str(e)}")


# Education endpoints
class EducationCreate(BaseModel):
    """Create education request."""
    user_email: EmailStr
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: str
    gpa: Optional[str] = None
    achievements: List[str] = []


@router.post("/education")
async def add_education(data: EducationCreate):
    """Add education to profile."""
    logger.info("Add education", email=data.user_email, institution=data.institution)
    
    try:
        # Check if profile exists
        profile = await UserProfileModel.find_one(UserProfileModel.email == data.user_email)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Create education
        education = EducationModel(
            user_email=data.user_email,
            institution=data.institution,
            degree=data.degree,
            field_of_study=data.field_of_study,
            start_date=data.start_date,
            end_date=data.end_date,
            gpa=data.gpa,
            achievements=data.achievements
        )
        
        await education.insert()
        logger.info("Education added", id=str(education.id))
        
        return {"id": str(education.id), "message": "Education added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to add education", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to add education: {str(e)}")
