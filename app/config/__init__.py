"""This module is responsible for loading the application configuration and setting up logging."""

from .config import get_settings
from .log import setup_logging

__all__ = ["get_settings", "setup_logging"]
