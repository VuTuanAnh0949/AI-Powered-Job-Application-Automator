"""
ATS (Applicant Tracking System) Scoring Service
Analyzes resume-job match using keyword matching and semantic similarity
"""
import structlog
from typing import Dict, List, Set, Tuple
import re
from collections import Counter
from datetime import datetime

from app.models.mongodb_models import UserProfile, JobListing, ATSAnalysis
from app.db.vector_db import vector_db

logger = structlog.get_logger(__name__)


class ATSService:
    """Service for ATS scoring and analysis"""
    
    def __init__(self):
        # Common stop words to filter out
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'you', 'your', 'our', 'we', 'us'
        }
    
    async def analyze_resume_match(
        self,
        user: UserProfile,
        job: JobListing
    ) -> ATSAnalysis:
        """
        Comprehensive ATS analysis of resume-job match
        Combines keyword matching and semantic similarity
        """
        resume_text = user.resume_text or ""
        job_text = f"{job.title} {job.description} {' '.join(job.skills_required or [])}"
        
        # 1. Keyword Analysis
        keyword_score, matched_keywords, missing_keywords = self._analyze_keywords(
            resume_text, job_text, job.skills_required or []
        )
        
        # 2. Semantic Similarity Score
        semantic_score = await self._calculate_semantic_similarity(resume_text, job_text)
        
        # 3. Experience Match
        experience_score = self._analyze_experience(user, job)
        
        # 4. Skills Match
        skills_score = self._analyze_skills(user.skills or [], job.skills_required or [])
        
        # 5. Overall Score (weighted average)
        overall_score = (
            keyword_score * 0.30 +      # 30% keyword matching
            semantic_score * 0.30 +      # 30% semantic similarity
            experience_score * 0.20 +    # 20% experience
            skills_score * 0.20          # 20% skills
        )
        
        # 6. Generate recommendations
        recommendations = self._generate_recommendations(
            overall_score=overall_score,
            keyword_score=keyword_score,
            semantic_score=semantic_score,
            experience_score=experience_score,
            skills_score=skills_score,
            missing_keywords=missing_keywords,
            user=user,
            job=job
        )
        
        # Create analysis record
        analysis = ATSAnalysis(
            user_email=user.email,
            job_id=str(job.id),
            overall_score=round(overall_score, 1),
            keyword_match_score=round(keyword_score, 1),
            experience_match_score=round(experience_score, 1),
            skills_match_score=round(skills_score, 1),
            semantic_similarity_score=round(semantic_score, 1),
            matched_keywords=list(matched_keywords),
            missing_keywords=list(missing_keywords),
            recommendations=recommendations
        )
        
        await analysis.insert()
        
        logger.info(
            "ats_analysis_complete",
            user=user.email,
            job_id=str(job.id),
            score=overall_score
        )
        
        return analysis
    
    def _extract_keywords(self, text: str, min_length: int = 3) -> Set[str]:
        """Extract keywords from text"""
        # Lowercase and remove special characters
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s+#]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Filter stop words and short words
        keywords = {
            word for word in words
            if len(word) >= min_length and word not in self.stop_words
        }
        
        return keywords
    
    def _analyze_keywords(
        self,
        resume: str,
        job_description: str,
        required_skills: List[str]
    ) -> Tuple[float, Set[str], Set[str]]:
        """
        Analyze keyword match between resume and job
        Returns: (score, matched_keywords, missing_keywords)
        """
        resume_keywords = self._extract_keywords(resume)
        job_keywords = self._extract_keywords(job_description)
        
        # Normalize required skills
        required_keywords = {skill.lower().strip() for skill in required_skills}
        
        # All important keywords from job
        all_job_keywords = job_keywords | required_keywords
        
        # Find matches
        matched = resume_keywords & all_job_keywords
        missing = all_job_keywords - resume_keywords
        
        # Calculate score (percentage of job keywords found in resume)
        if not all_job_keywords:
            score = 100.0
        else:
            score = (len(matched) / len(all_job_keywords)) * 100
        
        return score, matched, missing
    
    async def _calculate_semantic_similarity(
        self,
        resume: str,
        job_description: str
    ) -> float:
        """Calculate semantic similarity using vector embeddings"""
        try:
            # Encode both texts
            resume_vector = vector_db.encode_text(resume)
            job_vector = vector_db.encode_text(job_description)
            
            # Calculate cosine similarity
            import numpy as np
            similarity = np.dot(resume_vector, job_vector) / (
                np.linalg.norm(resume_vector) * np.linalg.norm(job_vector)
            )
            
            # Convert to percentage (0-100)
            score = float(similarity) * 100
            return max(0.0, min(100.0, score))
            
        except Exception as e:
            logger.error("semantic_similarity_failed", error=str(e))
            return 50.0  # Default to neutral score
    
    def _analyze_experience(self, user: UserProfile, job: JobListing) -> float:
        """Analyze experience match"""
        user_experience = user.years_of_experience or 0
        
        # Extract years from job requirements
        required_experience = self._extract_years_from_text(job.description)
        
        if required_experience is None:
            # No specific requirement, base on seniority
            if "senior" in job.title.lower():
                required_experience = 5
            elif "lead" in job.title.lower() or "principal" in job.title.lower():
                required_experience = 7
            elif "junior" in job.title.lower():
                required_experience = 1
            else:
                required_experience = 3  # Default mid-level
        
        # Score based on how close user's experience is to requirement
        if user_experience >= required_experience:
            # Over-qualified: still good but slight penalty if way over
            excess = user_experience - required_experience
            if excess > 5:
                score = 90.0  # Over-qualified
            else:
                score = 100.0  # Perfect match
        else:
            # Under-qualified: score decreases with gap
            gap = required_experience - user_experience
            score = max(0, 100 - (gap * 15))  # -15 points per year short
        
        return score
    
    def _extract_years_from_text(self, text: str) -> int:
        """Extract required years of experience from text"""
        # Pattern: "3+ years", "5-7 years", "minimum 2 years"
        patterns = [
            r'(\d+)\+?\s*years?',
            r'minimum\s+(\d+)\s*years?',
            r'at least\s+(\d+)\s*years?',
            r'(\d+)-\d+\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        
        return None
    
    def _analyze_skills(self, user_skills: List[str], required_skills: List[str]) -> float:
        """Analyze skills match"""
        if not required_skills:
            return 100.0
        
        # Normalize skills
        user_skills_norm = {skill.lower().strip() for skill in user_skills}
        required_skills_norm = {skill.lower().strip() for skill in required_skills}
        
        # Find matches
        matched = user_skills_norm & required_skills_norm
        
        # Calculate score
        score = (len(matched) / len(required_skills_norm)) * 100
        return score
    
    def _generate_recommendations(
        self,
        overall_score: float,
        keyword_score: float,
        semantic_score: float,
        experience_score: float,
        skills_score: float,
        missing_keywords: Set[str],
        user: UserProfile,
        job: JobListing
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Overall assessment
        if overall_score >= 80:
            recommendations.append("✅ Strong match! Consider applying immediately.")
        elif overall_score >= 60:
            recommendations.append("⚠️ Good match with room for improvement. Consider tailoring your resume.")
        else:
            recommendations.append("❌ Weak match. Significant gaps need to be addressed.")
        
        # Keyword recommendations
        if keyword_score < 70:
            top_missing = list(missing_keywords)[:5]
            recommendations.append(
                f"📝 Add these important keywords to your resume: {', '.join(top_missing)}"
            )
        
        # Skills recommendations
        if skills_score < 70:
            user_skills_set = {s.lower() for s in (user.skills or [])}
            missing_skills = [
                s for s in (job.skills_required or [])
                if s.lower() not in user_skills_set
            ][:3]
            if missing_skills:
                recommendations.append(
                    f"🎯 Highlight or develop these skills: {', '.join(missing_skills)}"
                )
        
        # Experience recommendations
        if experience_score < 70:
            user_exp = user.years_of_experience or 0
            required_exp = self._extract_years_from_text(job.description) or 3
            
            if user_exp < required_exp:
                recommendations.append(
                    f"📅 Position requires ~{required_exp} years experience. "
                    f"Emphasize relevant projects and accomplishments."
                )
            else:
                recommendations.append(
                    "📅 Your experience level exceeds requirements. "
                    "Focus on recent, relevant achievements."
                )
        
        # Semantic similarity
        if semantic_score < 60:
            recommendations.append(
                "🔄 Reframe your experience using terminology from the job description."
            )
        
        # Application status
        if job.applicant_count and job.applicant_count > 100:
            recommendations.append(
                f"⚡ {job.applicant_count} applicants. Apply quickly and stand out!"
            )
        
        return recommendations
    
    async def get_analysis(self, user_email: str, job_id: str) -> ATSAnalysis:
        """Get existing analysis or create new one"""
        # Try to find existing analysis
        analysis = await ATSAnalysis.find_one(
            ATSAnalysis.user_email == user_email,
            ATSAnalysis.job_id == job_id
        )
        
        if analysis:
            return analysis
        
        # Create new analysis
        from app.models.mongodb_models import UserProfile, JobListing
        user = await UserProfile.find_one(UserProfile.email == user_email)
        job = await JobListing.get(job_id)
        
        if not user or not job:
            raise ValueError("User or job not found")
        
        return await self.analyze_resume_match(user, job)
    
    async def batch_analyze(
        self,
        user: UserProfile,
        job_ids: List[str]
    ) -> List[ATSAnalysis]:
        """Analyze multiple jobs for a user"""
        analyses = []
        
        for job_id in job_ids:
            try:
                job = await JobListing.get(job_id)
                if not job:
                    logger.warning("job_not_found", job_id=job_id)
                    continue
                
                analysis = await self.analyze_resume_match(user, job)
                analyses.append(analysis)
                
            except Exception as e:
                logger.error("batch_analysis_failed", job_id=job_id, error=str(e))
        
        logger.info("batch_analysis_complete", user=user.email, count=len(analyses))
        return analyses


# Global service instance
ats_service = ATSService()


async def get_ats_service() -> ATSService:
    """Dependency for getting ATS service"""
    return ats_service
