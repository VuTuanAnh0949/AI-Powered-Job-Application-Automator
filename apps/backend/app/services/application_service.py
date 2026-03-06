"""
Application Tracking Service
Manages job applications throughout their lifecycle
"""
import structlog
from typing import Optional, List, Dict, Any
from datetime import datetime
from beanie.operators import In

from app.models.mongodb_models import Application, ApplicationStatus, UserProfile, JobListing

logger = structlog.get_logger(__name__)


class ApplicationService:
    """Service for managing job applications"""
    
    async def create_application(
        self,
        user_email: str,
        job_id: str,
        resume_doc_id: Optional[str] = None,
        cover_letter_doc_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Application:
        """Create a new application"""
        
        # Verify user and job exist
        user = await UserProfile.find_one(UserProfile.email == user_email)
        if not user:
            raise ValueError(f"User not found: {user_email}")
        
        job = await JobListing.get(job_id)
        if not job:
            raise ValueError(f"Job not found: {job_id}")
        
        # Check for duplicate application
        existing = await Application.find_one(
            Application.user_email == user_email,
            Application.job_id == job_id
        )
        
        if existing:
            logger.warning("duplicate_application", user=user_email, job_id=job_id)
            return existing
        
        # Create application
        application = Application(
            user_email=user_email,
            job_id=job_id,
            company=job.company,
            position=job.title,
            status=ApplicationStatus.DRAFT,
            resume_doc_id=resume_doc_id,
            cover_letter_doc_id=cover_letter_doc_id,
            notes=notes
        )
        
        await application.insert()
        
        logger.info("application_created", user=user_email, job_id=job_id)
        return application
    
    async def get_application(self, application_id: str) -> Optional[Application]:
        """Get application by ID"""
        return await Application.get(application_id)
    
    async def get_user_applications(
        self,
        user_email: str,
        status: Optional[ApplicationStatus] = None,
        limit: int = 100
    ) -> List[Application]:
        """Get all applications for a user"""
        query = Application.find(Application.user_email == user_email)
        
        if status:
            query = query.find(Application.status == status)
        
        applications = await query.sort(-Application.applied_date).limit(limit).to_list()
        
        logger.info("applications_retrieved", user=user_email, count=len(applications))
        return applications
    
    async def update_status(
        self,
        application_id: str,
        new_status: ApplicationStatus,
        notes: Optional[str] = None
    ) -> Application:
        """Update application status"""
        application = await self.get_application(application_id)
        if not application:
            raise ValueError(f"Application not found: {application_id}")
        
        old_status = application.status
        application.status = new_status
        
        # Update timestamps based on status
        if new_status == ApplicationStatus.SUBMITTED and not application.applied_date:
            application.applied_date = datetime.utcnow()
        elif new_status == ApplicationStatus.INTERVIEW:
            if not application.interview_date:
                application.interview_date = datetime.utcnow()
        elif new_status in [ApplicationStatus.OFFERED, ApplicationStatus.ACCEPTED]:
            if not application.offer_date:
                application.offer_date = datetime.utcnow()
        elif new_status == ApplicationStatus.REJECTED:
            if not application.rejection_date:
                application.rejection_date = datetime.utcnow()
        
        # Add notes if provided
        if notes:
            if application.notes:
                application.notes += f"\n\n[{datetime.utcnow().isoformat()}] {notes}"
            else:
                application.notes = notes
        
        await application.save()
        
        logger.info(
            "application_status_updated",
            application_id=application_id,
            old_status=old_status,
            new_status=new_status
        )
        
        return application
    
    async def submit_application(
        self,
        application_id: str,
        apply_url: Optional[str] = None
    ) -> Application:
        """Submit an application"""
        application = await self.get_application(application_id)
        if not application:
            raise ValueError(f"Application not found: {application_id}")
        
        if application.status != ApplicationStatus.DRAFT:
            raise ValueError("Only draft applications can be submitted")
        
        application.status = ApplicationStatus.SUBMITTED
        application.applied_date = datetime.utcnow()
        
        if apply_url:
            application.apply_url = apply_url
        
        await application.save()
        
        logger.info("application_submitted", application_id=application_id)
        return application
    
    async def schedule_interview(
        self,
        application_id: str,
        interview_date: datetime,
        interview_notes: Optional[str] = None
    ) -> Application:
        """Schedule an interview"""
        application = await self.update_status(
            application_id,
            ApplicationStatus.INTERVIEW,
            notes=f"Interview scheduled for {interview_date.isoformat()}\n{interview_notes or ''}"
        )
        
        application.interview_date = interview_date
        await application.save()
        
        logger.info("interview_scheduled", application_id=application_id, date=interview_date)
        return application
    
    async def record_rejection(
        self,
        application_id: str,
        rejection_reason: Optional[str] = None
    ) -> Application:
        """Record application rejection"""
        notes = f"Rejection recorded: {rejection_reason}" if rejection_reason else "Application rejected"
        
        application = await self.update_status(
            application_id,
            ApplicationStatus.REJECTED,
            notes=notes
        )
        
        logger.info("application_rejected", application_id=application_id)
        return application
    
    async def record_offer(
        self,
        application_id: str,
        salary_offered: Optional[float] = None,
        offer_details: Optional[str] = None
    ) -> Application:
        """Record job offer"""
        notes = "Offer received"
        if salary_offered:
            notes += f" - Salary: ${salary_offered:,.0f}"
        if offer_details:
            notes += f"\n{offer_details}"
        
        application = await self.update_status(
            application_id,
            ApplicationStatus.OFFERED,
            notes=notes
        )
        
        application.salary_offered = salary_offered
        await application.save()
        
        logger.info("offer_recorded", application_id=application_id, salary=salary_offered)
        return application
    
    async def accept_offer(
        self,
        application_id: str,
        notes: Optional[str] = None
    ) -> Application:
        """Accept job offer"""
        application = await self.update_status(
            application_id,
            ApplicationStatus.ACCEPTED,
            notes=notes or "Offer accepted"
        )
        
        logger.info("offer_accepted", application_id=application_id)
        return application
    
    async def delete_application(self, application_id: str) -> bool:
        """Delete an application"""
        try:
            application = await self.get_application(application_id)
            if not application:
                return False
            
            await application.delete()
            
            logger.info("application_deleted", application_id=application_id)
            return True
            
        except Exception as e:
            logger.error("application_delete_failed", application_id=application_id, error=str(e))
            return False
    
    async def get_statistics(self, user_email: str) -> Dict[str, Any]:
        """Get application statistics for a user"""
        applications = await Application.find(
            Application.user_email == user_email
        ).to_list()
        
        total = len(applications)
        
        # Count by status
        status_counts = {}
        for status in ApplicationStatus:
            count = sum(1 for app in applications if app.status == status)
            status_counts[status.value] = count
        
        # Calculate success metrics
        submitted = status_counts.get("submitted", 0)
        interviews = status_counts.get("interview", 0)
        offers = status_counts.get("offered", 0) + status_counts.get("accepted", 0)
        
        interview_rate = (interviews / submitted * 100) if submitted > 0 else 0
        offer_rate = (offers / submitted * 100) if submitted > 0 else 0
        
        # Recent activity
        recent_apps = sorted(applications, key=lambda x: x.applied_date or datetime.min, reverse=True)[:5]
        
        stats = {
            "total_applications": total,
            "status_breakdown": status_counts,
            "submitted_count": submitted,
            "interview_count": interviews,
            "offer_count": offers,
            "interview_rate": round(interview_rate, 1),
            "offer_rate": round(offer_rate, 1),
            "recent_applications": [
                {
                    "id": str(app.id),
                    "company": app.company,
                    "position": app.position,
                    "status": app.status.value,
                    "applied_date": app.applied_date.isoformat() if app.applied_date else None
                }
                for app in recent_apps
            ]
        }
        
        logger.info("statistics_generated", user=user_email, total=total)
        return stats
    
    async def get_applications_by_status(
        self,
        user_email: str,
        statuses: List[ApplicationStatus]
    ) -> List[Application]:
        """Get applications with specific statuses"""
        applications = await Application.find(
            Application.user_email == user_email,
            In(Application.status, statuses)
        ).to_list()
        
        return applications
    
    async def bulk_update_status(
        self,
        application_ids: List[str],
        new_status: ApplicationStatus
    ) -> int:
        """Update status for multiple applications"""
        count = 0
        
        for app_id in application_ids:
            try:
                await self.update_status(app_id, new_status)
                count += 1
            except Exception as e:
                logger.error("bulk_update_failed", application_id=app_id, error=str(e))
        
        logger.info("bulk_update_complete", updated=count, total=len(application_ids))
        return count


# Global service instance
application_service = ApplicationService()


async def get_application_service() -> ApplicationService:
    """Dependency for getting application service"""
    return application_service
