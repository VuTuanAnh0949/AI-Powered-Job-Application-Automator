"""
MongoDB Database Configuration and Connection
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import structlog
from typing import Optional

from app.core.config import settings

logger = structlog.get_logger(__name__)


class Database:
    """MongoDB database manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect(cls):
        """Connect to MongoDB"""
        try:
            logger.info("connecting_to_mongodb", url=settings.MONGODB_URL)
            
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                maxPoolSize=10,
                minPoolSize=1,
            )
            
            # Ping to verify connection
            await cls.client.admin.command('ping')
            
            logger.info("mongodb_connected")
            
        except Exception as e:
            logger.error("mongodb_connection_failed", error=str(e))
            raise
    
    @classmethod
    async def init_beanie(cls, document_models: list):
        """Initialize Beanie ODM with document models"""
        try:
            database = cls.client[settings.MONGODB_DB_NAME]
            
            await init_beanie(
                database=database,
                document_models=document_models
            )
            
            logger.info("beanie_initialized", models_count=len(document_models))
            
        except Exception as e:
            logger.error("beanie_init_failed", error=str(e))
            raise
    
    @classmethod
    async def close(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            logger.info("mongodb_disconnected")
    
    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        """Get MongoDB client"""
        if not cls.client:
            raise RuntimeError("Database not initialized. Call connect() first.")
        return cls.client
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        return cls.client[settings.MONGODB_DB_NAME]


# Database instance
database = Database()


async def get_database():
    """Dependency for getting database"""
    return database.get_database()
