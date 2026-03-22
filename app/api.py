"""Main API root configuration."""

import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.config import get_settings, setup_logging
from app.routers import users

# Note: Load config and environment variables eagerly (it's being cached)
app_settings = get_settings()

setup_logging(log_level=app_settings.log_level)

app = FastAPI(
    title="My Small Python Project Template",
    description="Small Python project template",
    version="0.1.0",
)

# import additional routers
app.include_router(router=users.router, prefix="/api", tags=["users"])


@app.get("/")
async def root():
    """Simple root endpoint."""
    return {"message": "Welcome!"}


@app.get("/api")
async def api_root():
    """Simple API root endpoint."""
    return {"message": "Welcome to the API!"}


@app.get("/health")
async def health_check():
    """Simple health-check endpoint."""

    logger.debug("Debug")
    logger.info("Info")
    logger.warning("Warning")
    logger.error("Error")

    return {"message": "alive"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
