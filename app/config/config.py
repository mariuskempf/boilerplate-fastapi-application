"""Application Configuration Module."""

import logging
from functools import lru_cache
from logging.config import dictConfig

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


def setup_logging(log_level: str = "INFO") -> None:
    """Configure global logging for the application."""
    # Ensure uppercase
    log_level = log_level.upper()

    # Validate log_level, fallback to INFO if invalid
    valid_levels = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
    if log_level not in valid_levels:
        print(f"Invalid LOG_LEVEL '{log_level}' — falling back to INFO")
        log_level = "INFO"

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,  # Keep FastAPI, Uvicorn, etc. logging
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console"],
            },
        }
    )

    logger = logging.getLogger(__name__)
    logger.info("Logging has been configured at level '%s'", log_level)
