"""Health check endpoints"""

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response schema"""

    status: str = Field(..., description="Health status (healthy/unhealthy)")
    timestamp: datetime = Field(..., description="Current server timestamp")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment (development/production)")


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse: API health status and metadata

    Example:
        GET /api/health
        {
            "status": "healthy",
            "timestamp": "2025-12-28T12:00:00Z",
            "version": "2.0.0",
            "environment": "development"
        }
    """
    from app.config import settings

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        version="2.0.0",
        environment=settings.ENVIRONMENT,
    )
