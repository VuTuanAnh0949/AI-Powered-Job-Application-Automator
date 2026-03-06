"""Document generation endpoints (resumes, cover letters)."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from pydantic import BaseModel, Field
import structlog

from app.services.ai_service import AIService, get_ai_service
from app.models.mongodb_models import UserProfile, JobListing, GeneratedDocument as DocModel

logger = structlog.get_logger()
router = APIRouter()


class GenerateResumeRequest(BaseModel):
    """Generate resume request."""
    user_email: str
    job_id: Optional[str] = None
    template: Optional[str] = Field(default="modern", description="Resume template: modern, classic, minimal")
    ai_provider: Optional[str] = Field(default=None, description="AI provider: gemini, openai, groq")


class GenerateCoverLetterRequest(BaseModel):
    """Generate cover letter request."""
    user_email: str
    job_id: str
    ai_provider: Optional[str] = Field(default=None, description="AI provider: gemini, openai, groq")


class DocumentResponse(BaseModel):
    """Document generation response."""
    document_id: str
    document_type: str
    content_preview: str
    ai_provider: str
    created_at: str
    job_id: Optional[str] = None


@router.post("/resume/generate", response_model=DocumentResponse)
async def generate_resume(
    request: GenerateResumeRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Generate AI-tailored resume for a specific job.
    
    The AI will:
    1. Analyze job requirements (if job provided)
    2. Match your experience to job needs
    3. Highlight relevant skills and achievements
    4. Optimize for ATS (Applicant Tracking Systems)
    5. Format professionally
    """
    logger.info("Generate resume", user=request.user_email, job_id=request.job_id)
    
    try:
        # Get user profile
        user = await UserProfile.find_one(UserProfile.email == request.user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get job if specified
        job = None
        if request.job_id:
            job = await JobListing.get(request.job_id)
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")
        
        # Generate resume
        doc = await ai_service.generate_resume(user, job, request.ai_provider)
        
        return DocumentResponse(
            document_id=str(doc.id),
            document_type="resume",
            content_preview=doc.content_text[:500] + "..." if len(doc.content_text) > 500 else doc.content_text,
            ai_provider=doc.ai_provider,
            created_at=doc.created_at.isoformat(),
            job_id=doc.job_id
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Resume generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")


@router.post("/cover-letter/generate", response_model=DocumentResponse)
async def generate_cover_letter(
    request: GenerateCoverLetterRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Generate AI-tailored cover letter for a specific job.
    
    The AI will:
    1. Analyze company and role
    2. Craft compelling opening statement
    3. Connect your experience to job requirements
    4. Show genuine interest and enthusiasm
    5. Include professional closing
    """
    logger.info("Generate cover letter", user=request.user_email, job_id=request.job_id)
    
    try:
        # Get user profile
        user = await UserProfile.find_one(UserProfile.email == request.user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get job
        job = await JobListing.get(request.job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Generate cover letter
        doc = await ai_service.generate_cover_letter(user, job, request.ai_provider)
        
        return DocumentResponse(
            document_id=str(doc.id),
            document_type="cover_letter",
            content_preview=doc.content_text[:500] + "..." if len(doc.content_text) > 500 else doc.content_text,
            ai_provider=doc.ai_provider,
            created_at=doc.created_at.isoformat(),
            job_id=doc.job_id
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Cover letter generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Cover letter generation failed: {str(e)}")


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """Get document details."""
    logger.info("Get document", document_id=document_id)
    
    try:
        doc = await DocModel.get(document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return DocumentResponse(
            document_id=str(doc.id),
            document_type=doc.document_type,
            content_preview=doc.content_text[:500] + "..." if len(doc.content_text) > 500 else doc.content_text,
            ai_provider=doc.ai_provider,
            created_at=doc.created_at.isoformat(),
            job_id=doc.job_id
        )
        
    except Exception as e:
        logger.error("Get document failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}/full")
async def get_full_document(document_id: str):
    """Get full document content."""
    logger.info("Get full document", document_id=document_id)
    
    try:
        doc = await DocModel.get(document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "document_id": str(doc.id),
            "document_type": doc.document_type,
            "content_text": doc.content_text,
            "content_html": doc.content_html,
            "ai_provider": doc.ai_provider,
            "created_at": doc.created_at.isoformat(),
            "job_id": doc.job_id,
            "user_email": doc.user_email
        }
        
    except Exception as e:
        logger.error("Get full document failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def list_documents(
    user_email: str = Query(..., description="User email"),
    document_type: Optional[str] = Query(None, description="Filter by type: resume, cover_letter"),
    limit: int = Query(50, ge=1, le=200)
):
    """List user's generated documents."""
    logger.info("List documents", user=user_email, type=document_type)
    
    try:
        query = DocModel.find(DocModel.user_email == user_email)
        
        if document_type:
            query = query.find(DocModel.document_type == document_type)
        
        docs = await query.sort(-DocModel.created_at).limit(limit).to_list()
        
        return {
            "total": len(docs),
            "documents": [
                DocumentResponse(
                    document_id=str(doc.id),
                    document_type=doc.document_type,
                    content_preview=doc.content_text[:200] + "..." if len(doc.content_text) > 200 else doc.content_text,
                    ai_provider=doc.ai_provider,
                    created_at=doc.created_at.isoformat(),
                    job_id=doc.job_id
                )
                for doc in docs
            ]
        }
        
    except Exception as e:
        logger.error("List documents failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document."""
    logger.info("Delete document", document_id=document_id)
    
    try:
        doc = await DocModel.get(document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        await doc.delete()
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        logger.error("Delete document failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
