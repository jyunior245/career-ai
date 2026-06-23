import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./career_ai.db")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Groq Configuration
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # File Upload Constraints
    MAX_PDF_SIZE_MB: int = 10
    MAX_RESUME_TEXT_LENGTH: int = 50000
    MIN_RESUME_TEXT_LENGTH: int = 100
    MAX_JOB_DESCRIPTION_LENGTH: int = 10000
    MIN_JOB_DESCRIPTION_LENGTH: int = 50
    UPLOAD_DIR: str = "backend/uploads"
    
    # Performance
    API_TIMEOUT: int = 30  # Ollama might take longer


settings = Settings()
