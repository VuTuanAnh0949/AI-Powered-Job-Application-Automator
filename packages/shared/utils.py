"""Shared utility functions."""

import re
from typing import List, Dict, Any
import structlog

logger = structlog.get_logger()


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s\.\,\-\(\)]', '', text)
    return text.strip()


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """Extract keywords from text."""
    # Simple keyword extraction
    words = text.lower().split()
    keywords = [w for w in words if len(w) >= min_length]
    return list(set(keywords))


def calculate_match_score(
    job_keywords: List[str],
    profile_keywords: List[str]
) -> float:
    """Calculate job match score based on keyword overlap."""
    if not job_keywords or not profile_keywords:
        return 0.0
    
    job_set = set(job_keywords)
    profile_set = set(profile_keywords)
    
    overlap = len(job_set.intersection(profile_set))
    total = len(job_set.union(profile_set))
    
    return overlap / total if total > 0 else 0.0


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount."""
    if currency == "USD":
        return f"${amount:,.0f}"
    return f"{amount:,.0f} {currency}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe filesystem operations."""
    # Replace spaces and special characters
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename.strip('_')
