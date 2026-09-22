import os
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Vidwan Classes API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "dev_secret_key_vidwan_classes_fullstack_2026"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Backend URL for static media serving if local
    BACKEND_URL: str = "http://localhost:8000"

    # CORS
    FRONTEND_URL: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5500,http://localhost:8000"

    @property
    def cors_origins(self) -> List[str]:
        if isinstance(self.FRONTEND_URL, str):
            return [url.strip() for url in self.FRONTEND_URL.split(",") if url.strip()]
        return ["*"]

    # Database
    DATABASE_URL: str = "sqlite:///./vidwan.db"

    # Email Config
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    ADMIN_EMAIL: str = "admin@vidwanclasses.com"
    FROM_EMAIL: str = "noreply@vidwanclasses.com"

    # Storage Config
    STORAGE_PROVIDER: str = "local"  # local, cloudinary, supabase, s3
    STORAGE_BUCKET: str = "vidwan-assets"
    STORAGE_ACCESS_KEY: str = ""
    STORAGE_SECRET_KEY: str = ""
    STORAGE_URL_PREFIX: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
