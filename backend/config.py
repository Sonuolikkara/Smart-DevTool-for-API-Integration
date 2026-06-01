"""
Configuration management for Smart DevTool backend
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # API Configuration
    API_TITLE: str = "Smart DevTool for API Integration"
    API_VERSION: str = "1.0.0"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_PRIMARY_MODEL: str = "qwen2.5-coder"
    OLLAMA_FALLBACK_MODEL: str = "llama3"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"
    
    # Database Configuration
    CHROMADB_PATH: str = "./data/chromadb"
    
    # Scraping Configuration
    PLAYWRIGHT_HEADLESS: bool = True
    REQUEST_TIMEOUT: int = 30
    
    # Processing Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings
settings = Settings()
