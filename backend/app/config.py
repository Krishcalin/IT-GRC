"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "IT-GRC Portal"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://grc:changeme@db:5432/itgrc"

    # Auth / JWT
    SECRET_KEY: str = "change-this-to-a-random-64-char-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # First superuser
    FIRST_SUPERUSER_EMAIL: str = "admin@company.com"
    FIRST_SUPERUSER_PASSWORD: str = "Admin@123"

    # SAML / OIDC (optional)
    SAML_METADATA_URL: str = ""
    OIDC_DISCOVERY_URL: str = ""
    OIDC_CLIENT_ID: str = ""
    OIDC_CLIENT_SECRET: str = ""

    # File uploads
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 50

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
