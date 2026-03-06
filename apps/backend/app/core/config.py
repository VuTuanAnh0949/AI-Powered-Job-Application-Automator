"""Application configuration."""

from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application
    PROJECT_NAME: str = "AutoApply AI"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=True)
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
        description="Allowed CORS origins"
    )
    
    # Database - MongoDB
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection URL"
    )
    MONGODB_DB_NAME: str = Field(
        default="autoapply_ai",
        description="MongoDB database name"
    )
    
    # Vector Database - Qdrant
    QDRANT_URL: str = Field(
        default="http://localhost:6333",
        description="Qdrant server URL"
    )
    QDRANT_API_KEY: str = Field(
        default="",
        description="Qdrant API key (for cloud)"
    )
    QDRANT_COLLECTION_NAME: str = Field(
        default="job_embeddings",
        description="Qdrant collection name"
    )
    
    # AI/LLM
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key")
    GROQ_API_KEY: str = Field(default="", description="Groq API key")
    
    # Default LLM provider
    DEFAULT_LLM_PROVIDER: str = Field(default="gemini", description="Default LLM provider: openai, gemini, groq")
    
    # Job Search
    LINKEDIN_EMAIL: str = Field(default="", description="LinkedIn login email")
    LINKEDIN_PASSWORD: str = Field(default="", description="LinkedIn login password")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./data/uploads", description="Upload directory")
    GENERATED_DOCS_DIR: str = Field(default="./data/generated_docs", description="Generated documents directory")
    
    # Redis (optional, for caching)
    REDIS_URL: str = Field(default="redis://localhost:6379", description="Redis connection URL")
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-here-change-in-production", description="Secret key for JWT")
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration in minutes")


settings = Settings()
