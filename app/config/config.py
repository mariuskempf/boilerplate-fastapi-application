"""Application Configuration Module."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Overall settings for the application.

    This reads set environment variables. Either from th environment or from the '.env' file (dev).

    Note:
    Environment variables will always take priority over values loaded from a dotenv file.

    See Pydantic documentation:
        https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support
    """

    # Use .env for local development
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Add environment variables here - e.g.:

    # azure_openai_endpoint: str
    # azure_openai_api_version: str = "2024-12-01-preview"  # Or your specific version
    # ...

    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Load app configuration"""
    return Settings()  # type: ignore
