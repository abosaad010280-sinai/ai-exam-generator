"""Configuration settings for the application"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # FastAPI
    APP_NAME: str = "منصة إنشاء الامتحانات بالذكاء الاصطناعي"
    APP_DESCRIPTION: str = "AI Exam Generator Platform"
    APP_VERSION: str = "1.0.0"
    FASTAPI_ENV: str = "development"
    DEBUG: bool = True

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # Database
    DATABASE_URL: str = "sqlite:///./database/exam.db"

    # Upload Settings
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: list = ["pdf", "docx", "txt"]

    # File Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOAD_FOLDER: str = "uploads"
    EXPORT_FOLDER: str = "exports"
    DATABASE_FOLDER: str = "database"

    # Similarity Threshold
    SIMILARITY_THRESHOLD: float = 0.80

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **data):
        super().__init__(**data)
        # Create directories if they don't exist
        for folder in [self.UPLOAD_FOLDER, self.EXPORT_FOLDER, self.DATABASE_FOLDER, "logs"]:
            path = self.BASE_DIR / folder
            path.mkdir(exist_ok=True)


# Load settings
settings = Settings()
