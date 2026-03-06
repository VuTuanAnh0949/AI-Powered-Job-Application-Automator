"""
Vector Database Configuration using Qdrant
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import structlog
from typing import List, Optional, Dict, Any
import uuid

from app.core.config import settings

logger = structlog.get_logger(__name__)


class VectorDatabase:
    """Qdrant vector database manager"""
    
    def __init__(self):
        self.client: Optional[QdrantClient] = None
        self.encoder: Optional[SentenceTransformer] = None
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.vector_size = 384  # all-MiniLM-L6-v2 dimension
    
    async def connect(self):
        """Connect to Qdrant and initialize encoder"""
        try:
            logger.info("connecting_to_qdrant", url=settings.QDRANT_URL)
            
            # Initialize Qdrant client
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None,
            )
            
            # Initialize sentence transformer for embeddings
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Create collection if not exists
            await self._ensure_collection()
            
            logger.info("qdrant_connected")
            
        except Exception as e:
            logger.error("qdrant_connection_failed", error=str(e))
            raise
    
    async def _ensure_collection(self):
        """Ensure collection exists, create if not"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info("collection_created", name=self.collection_name)
            else:
                logger.info("collection_exists", name=self.collection_name)
                
        except Exception as e:
            logger.error("collection_setup_failed", error=str(e))
            raise
    
    def encode_text(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        if not self.encoder:
            raise RuntimeError("Encoder not initialized")
        
        vector = self.encoder.encode(text).tolist()
        return vector
    
    async def add_job(
        self,
        job_id: str,
        title: str,
        description: str,
        company: str,
        location: str,
        metadata: Dict[str, Any] = None
    ):
        """Add job to vector database"""
        try:
            # Combined text for better semantic search
            combined_text = f"{title} {company} {description} {location}"
            vector = self.encode_text(combined_text)
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "job_id": job_id,
                    "title": title,
                    "company": company,
                    "location": location,
                    "description": description[:500],  # Truncate for storage
                    **(metadata or {})
                }
            )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            logger.info("job_added_to_vector_db", job_id=job_id)
            
        except Exception as e:
            logger.error("add_job_failed", job_id=job_id, error=str(e))
            raise
    
    async def search_similar_jobs(
        self,
        query: str,
        limit: int = 10,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search for similar jobs using semantic search"""
        try:
            query_vector = self.encode_text(query)
            
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )
            
            jobs = []
            for result in results:
                job = {
                    **result.payload,
                    "similarity_score": result.score
                }
                jobs.append(job)
            
            logger.info("jobs_searched", query=query[:50], results_count=len(jobs))
            return jobs
            
        except Exception as e:
            logger.error("search_failed", error=str(e))
            return []
    
    async def search_by_resume(
        self,
        resume_text: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Find matching jobs based on resume content"""
        return await self.search_similar_jobs(resume_text, limit=limit)
    
    async def delete_job(self, job_id: str):
        """Delete job from vector database"""
        try:
            # Find points with matching job_id
            results = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter={
                    "must": [
                        {"key": "job_id", "match": {"value": job_id}}
                    ]
                },
                limit=100
            )
            
            point_ids = [point.id for point in results[0]]
            
            if point_ids:
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=point_ids
                )
                logger.info("job_deleted_from_vector_db", job_id=job_id)
            
        except Exception as e:
            logger.error("delete_job_failed", job_id=job_id, error=str(e))
    
    async def close(self):
        """Close connection"""
        if self.client:
            self.client.close()
            logger.info("qdrant_disconnected")


# Global instance
vector_db = VectorDatabase()


async def get_vector_db() -> VectorDatabase:
    """Dependency for getting vector database"""
    return vector_db
