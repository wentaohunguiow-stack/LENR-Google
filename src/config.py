"""Configuration management for the RAG system."""

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    google_api_key: str
    default_model: str = "gemini-2.5-flash"
    default_store_name: str = "default-store"
    max_file_size_mb: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


def get_api_key() -> str:
    """Get Google API key from environment."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment. "
            "Please set it in .env file or as an environment variable."
        )
    return api_key
