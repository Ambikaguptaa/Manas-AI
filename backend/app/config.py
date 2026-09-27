"""
Application Configuration Module
Handles environment variables and system settings using Pydantic V2 Settings.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    PROJECT_NAME: str = "AI Mental Wellness System Using Indian Psychology"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    
    # CORS Origins allowed for Frontend integration
    ALLOWED_ORIGINS: List[str] = [
        "https://manas-ai-kappa.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # SQLite Database URL
    DATABASE_URL: str = "sqlite:///./manas_wellness.db"
    
    # Academic Disclaimer constant
    DISCLAIMER_TEXT: str = (
        "This system is strictly an academic mental wellness self-reflection tool "
        "rooted in Indian Knowledge Systems (IKS). It does NOT constitute medical, "
        "psychiatric, or psychological diagnosis or clinical therapy."
    )


settings = Settings()
