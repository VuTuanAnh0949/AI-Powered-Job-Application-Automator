"""Configuration settings for LLM integration."""
import os
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv

load_dotenv()

class LlamaConfig(BaseModel):
    use_api: bool = Field(default=os.getenv("LLAMA_USE_API", "true").lower() == "true")
    api_provider: Optional[str] = Field(default=os.getenv("LLAMA_API_PROVIDER", "gemini"))
    api_model: Optional[str] = Field(default=os.getenv("LLAMA_API_MODEL", None))
    github_token: SecretStr = Field(default_factory=lambda: SecretStr(os.getenv("GITHUB_TOKEN", "")))
    groq_api_key: SecretStr = Field(default_factory=lambda: SecretStr(os.getenv("GROQ_API_KEY", "")))
    gemini_api_key: SecretStr = Field(default_factory=lambda: SecretStr(os.getenv("GEMINI_API_KEY", "")))
    openai_api_key: SecretStr = Field(default_factory=lambda: SecretStr(os.getenv("OPENAI_API_KEY", "")))
    temperature: float = Field(default=float(os.getenv("TEMPERATURE", "0.7")))
    max_tokens: int = Field(default=int(os.getenv("MAX_TOKENS", "4000")))
    
    def get_api_config(self) -> Optional[Dict[str, Any]]:
        """Get API configuration based on provider."""
        if not self.use_api:
            return None
            
        provider = (self.api_provider or "gemini").lower()
        
        # Determine model name
        if self.api_model:
            model = self.api_model
        elif provider == "gemini":
            model = "gemini-pro"
        elif provider == "groq":
            model = "llama-3.3-70b-versatile"
        elif provider == "openai":
            model = "gpt-4"
        elif provider == "github":
            model = "meta/Llama-4-Maverick-17B-128E-Instruct-FP8"
        else:
            model = "gemini-pro"
        
        # Get API key based on provider
        if provider == "gemini":
            api_key = self.gemini_api_key.get_secret_value()
            api_base = "https://generativelanguage.googleapis.com/v1beta"
        elif provider == "groq":
            api_key = self.groq_api_key.get_secret_value()
            api_base = "https://api.groq.com/openai/v1"
        elif provider == "openai":
            api_key = self.openai_api_key.get_secret_value()
            api_base = "https://api.openai.com/v1"
        elif provider == "github":
            api_key = self.github_token.get_secret_value()
            api_base = "https://models.inference.ai.azure.com"
        else:
            api_key = self.gemini_api_key.get_secret_value()
            api_base = "https://generativelanguage.googleapis.com/v1beta"
        
        if not api_key or api_key == "":
            return None
            
        return {
            "api_key": api_key,
            "api_base": api_base,
            "model": model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": 30,
            "provider": provider
        }
    
    @property
    def resume_template_prompt(self) -> str:
        """Default prompt template for resume generation."""
        return """
        Based on the following job description and candidate information, create a professional resume.
        
        Job Description:
        {job_description}
        
        Candidate Information:
        {candidate_info}
        
        Create a well-structured resume that highlights relevant skills and experiences.
        """
    
    @classmethod
    def from_env(cls):
        return cls()
