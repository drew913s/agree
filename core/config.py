"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Agree"
    app_env: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Security Keys
    secret_key: str = Field(..., min_length=32)
    jwt_secret_key: str = Field(..., min_length=32)
    signing_token_secret: str = Field(..., min_length=32)
    database_encryption_key: str = Field(..., min_length=32)

    # JWT Configuration
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7
    signing_token_expire_days: int = 7

    # Database
    database_url: str

    # Redis
    redis_url: str

    # Storage Backend
    storage_backend: str = "minio"  # minio or gcs

    # MinIO (Development)
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = ""
    minio_secret_key: str = ""
    minio_bucket_documents: str = "agree-documents"
    minio_bucket_signatures: str = "agree-signatures"
    minio_bucket_thumbnails: str = "agree-thumbnails"
    minio_secure: bool = False

    # Google Cloud Storage (Production)
    gcs_bucket_name: str = ""
    gcs_credentials_path: str = ""
    gcs_credentials_json: str = ""

    # SendGrid
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = ""
    sendgrid_from_name: str = "Agree Signing"
    sendgrid_sandbox_mode: bool = True

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-haiku-20240307"

    # Whisper
    whisper_model: str = "base"
    whisper_device: str = "cpu"

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests_per_minute: int = 100

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # File Upload
    max_upload_size_mb: int = 25
    allowed_extensions: str = "pdf"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1

    @field_validator("cors_origins")
    @classmethod
    def parse_cors_origins(cls, v: str) -> str:
        """Validate CORS origins format."""
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins as list."""
        return [o.strip() for o in self.cors_origins.split(",")]

    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions as list."""
        return [e.strip() for e in self.allowed_extensions.split(",")]

    @property
    def max_upload_size_bytes(self) -> int:
        """Max upload size in bytes."""
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
