"""
Pronto Casa - Configuration

Environment-based settings using Pydantic.
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Pronto Casa"
    DEBUG: bool = False
    ENV: str = "development"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/prontocasa"
    
    # Auth
    JWT_SECRET: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    APPLE_CLIENT_ID: str = ""
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    PLATFORM_FEE_PERCENT: float = 10.0  # 10% platform fee
    
    # Twilio
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # WhatsApp
    WHATSAPP_API_TOKEN: str = ""
    WHATSAPP_PHONE_ID: str = ""
    
    # Firebase (Push Notifications)
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_CREDENTIALS_PATH: str = ""
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "eu-south-1"
    S3_BUCKET_NAME: str = "prontocasa-media"
    
    # OpenAI (AI Diagnosis)
    OPENAI_API_KEY: str = ""
    
    # Google Maps
    GOOGLE_MAPS_API_KEY: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://prontocasa.it"]
    
    # Media settings
    MEDIA_RETENTION_DAYS: int = 10  # Auto-delete after 10 days
    MAX_PHOTOS_PER_REQUEST: int = 5
    MAX_VIDEO_DURATION_SECONDS: int = 10
    
    # Dispatch settings
    MAX_TECHNICIANS_TO_NOTIFY: int = 5
    QUOTE_REVISION_THRESHOLD_PERCENT: float = 40.0  # Require explanation if > 40%
    CANCELLATION_PENALTY_PERCENT: float = 20.0  # 5% app + 15% technician
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
