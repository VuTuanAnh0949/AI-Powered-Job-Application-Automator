"""
AI Service for Resume and Cover Letter Generation
Supports multiple providers: Gemini, OpenAI, Groq
"""
import structlog
from typing import Optional, Dict, Any, Literal
import google.generativeai as genai
from openai import AsyncOpenAI
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.models.mongodb_models import UserProfile, JobListing, GeneratedDocument

logger = structlog.get_logger(__name__)

AIProvider = Literal["gemini", "openai", "groq"]


class AIService:
    """AI service for generating resumes and cover letters"""
    
    def __init__(self):
        self.setup_providers()
    
    def setup_providers(self):
        """Initialize AI providers"""
        # Gemini
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("gemini_initialized")
        else:
            self.gemini = None
        
        # OpenAI
        if settings.OPENAI_API_KEY:
            self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("openai_initialized")
        else:
            self.openai = None
        
        # Groq
        if settings.GROQ_API_KEY:
            self.groq = AsyncGroq(api_key=settings.GROQ_API_KEY)
            logger.info("groq_initialized")
        else:
            self.groq = None
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_with_gemini(self, prompt: str) -> str:
        """Generate text using Gemini"""
        if not self.gemini:
            raise ValueError("Gemini API key not configured")
        
        response = await self.gemini.generate_content_async(prompt)
        return response.text
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_with_openai(self, prompt: str, model: str = "gpt-4-turbo-preview") -> str:
        """Generate text using OpenAI"""
        if not self.openai:
            raise ValueError("OpenAI API key not configured")
        
        response = await self.openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_with_groq(self, prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
        """Generate text using Groq"""
        if not self.groq:
            raise ValueError("Groq API key not configured")
        
        response = await self.groq.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    async def generate(
        self,
        prompt: str,
        provider: Optional[AIProvider] = None
    ) -> tuple[str, str]:
        """Generate text using specified or default provider"""
        provider = provider or settings.DEFAULT_LLM_PROVIDER
        
        try:
            if provider == "gemini":
                text = await self.generate_with_gemini(prompt)
            elif provider == "openai":
                text = await self.generate_with_openai(prompt)
            elif provider == "groq":
                text = await self.generate_with_groq(prompt)
            else:
                raise ValueError(f"Unknown provider: {provider}")
            
            logger.info("ai_generation_success", provider=provider)
            return text, provider
            
        except Exception as e:
            logger.error("ai_generation_failed", provider=provider, error=str(e))
            raise
    
    async def generate_resume(
        self,
        user_profile: UserProfile,
        job: Optional[JobListing] = None,
        provider: Optional[AIProvider] = None
    ) -> GeneratedDocument:
        """Generate tailored resume"""
        
        # Build prompt
        prompt = self._build_resume_prompt(user_profile, job)
        
        # Generate
        content, used_provider = await self.generate(prompt, provider)
        
        # Create document record
        doc = GeneratedDocument(
            user_email=user_profile.email,
            job_id=str(job.id) if job else None,
            document_type="resume",
            content_text=content,
            ai_provider=used_provider,
            prompt_used=prompt[:500]  # Store truncated prompt
        )
        
        await doc.insert()
        
        logger.info("resume_generated", user=user_profile.email, job_id=str(job.id) if job else None)
        return doc
    
    async def generate_cover_letter(
        self,
        user_profile: UserProfile,
        job: JobListing,
        provider: Optional[AIProvider] = None
    ) -> GeneratedDocument:
        """Generate tailored cover letter"""
        
        # Build prompt
        prompt = self._build_cover_letter_prompt(user_profile, job)
        
        # Generate
        content, used_provider = await self.generate(prompt, provider)
        
        # Create document record
        doc = GeneratedDocument(
            user_email=user_profile.email,
            job_id=str(job.id),
            document_type="cover_letter",
            content_text=content,
            ai_provider=used_provider,
            prompt_used=prompt[:500]
        )
        
        await doc.insert()
        
        logger.info("cover_letter_generated", user=user_profile.email, job_id=str(job.id))
        return doc
    
    def _build_resume_prompt(self, user: UserProfile, job: Optional[JobListing]) -> str:
        """Build resume generation prompt"""
        
        base_prompt = f"""
Generate a professional resume for the following candidate:

**Candidate Information:**
- Name: {user.full_name}
- Title: {user.title}
- Location: {user.location or 'Not specified'}
- Email: {user.email}
- Phone: {user.phone or 'Not specified'}
- LinkedIn: {user.linkedin_url or 'Not specified'}
- Summary: {user.summary or 'Not specified'}
- Years of Experience: {user.years_of_experience or 'Not specified'}

**Skills:**
{', '.join(user.skills) if user.skills else 'Not specified'}

**Resume Text:**
{user.resume_text or 'Not provided'}
"""
        
        if job:
            base_prompt += f"""

**Target Job:**
- Title: {job.title}
- Company: {job.company}
- Location: {job.location}
- Description: {job.description[:500]}...
- Required Skills: {', '.join(job.skills_required) if job.skills_required else 'Not specified'}

Please tailor the resume to highlight relevant experience and skills that match this job posting.
"""
        
        base_prompt += """

**Instructions:**
1. Format as a professional, ATS-friendly resume
2. Use clear section headings (Summary, Experience, Skills, Education)
3. Highlight achievements with quantifiable results
4. Tailor keywords to match the job description (if provided)
5. Keep it concise (1-2 pages)
6. Use strong action verbs

Generate the resume in markdown format.
"""
        
        return base_prompt
    
    def _build_cover_letter_prompt(self, user: UserProfile, job: JobListing) -> str:
        """Build cover letter generation prompt"""
        
        prompt = f"""
Generate a professional cover letter for the following application:

**Candidate:**
- Name: {user.full_name}
- Title: {user.title}
- Summary: {user.summary or 'Not specified'}

**Skills:**
{', '.join(user.skills[:10]) if user.skills else 'Not specified'}

**Job:**
- Title: {job.title}
- Company: {job.company}
- Location: {job.location}
- Description: {job.description[:800]}

**Instructions:**
1. Write a compelling, personalized cover letter
2. Address why the candidate is interested in this role
3. Highlight 2-3 key achievements or skills that match the job
4. Show enthusiasm for the company and role
5. Keep it to 3-4 paragraphs
6. Professional but not overly formal tone
7. Include a strong opening and closing

Generate the cover letter in markdown format with proper formatting for a professional letter (date, address, salutation, body, closing).
"""
        
        return prompt


# Global service instance
ai_service = AIService()


async def get_ai_service() -> AIService:
    """Dependency for getting AI service"""
    return ai_service
