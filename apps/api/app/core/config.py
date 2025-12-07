"""Application configuration handling."""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, RedisDsn, field_validator, validator
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Handwritten Answer Evaluation Platform"
    VERSION: str = "0.1.0"

    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000", "http://127.0.0.1:8000"])

    DATABASE_URL: str = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_handwritten", env="DATABASE_URL"
    )
    SYNC_DATABASE_URL: str = Field(
        "postgresql://postgres:postgres@localhost:5432/ai_handwritten", env="SYNC_DATABASE_URL"
    )
    REDIS_URL: RedisDsn = Field("redis://localhost:6379/0", env="REDIS_URL")

    SUPABASE_URL: str = Field("", env="SUPABASE_URL")
    SUPABASE_KEY: str = Field("", env="SUPABASE_KEY")
    SUPABASE_BUCKET: str = Field("answer-sheets", env="SUPABASE_BUCKET")

    JWT_SECRET_KEY: str = Field("change-me", env="JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = Field("change-me-refresh", env="JWT_REFRESH_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 7, env="REFRESH_TOKEN_EXPIRE_MINUTES")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")

    OCR_MODEL_EN: str = Field("microsoft/trocr-base-handwritten", env="OCR_MODEL_EN")
    OCR_MODEL_HI: str = Field("microsoft/trocr-base-handwritten-hi", env="OCR_MODEL_HI")
    SENTENCE_TRANSFORMER_MODEL: str = Field("sentence-transformers/all-MiniLM-L6-v2", env="SENTENCE_TRANSFORMER_MODEL")

    KW_WEIGHT: float = Field(0.5, env="KW_WEIGHT")
    SEM_WEIGHT: float = Field(0.5, env="SEM_WEIGHT")

    model_config = SettingsConfigDict(
        env_file=[".env", "../.env", "../../.env"], 
        case_sensitive=True
    )

    @field_validator("CORS_ORIGINS", mode="before")
    def parse_cors_origins(cls, value: str | List[AnyHttpUrl]):
        if isinstance(value, str) and not value.startswith("["):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

