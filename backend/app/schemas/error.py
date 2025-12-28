"""Standard API error response schemas"""

from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Individual error detail"""

    field: str = Field(..., description="Field that caused the error")
    message: str = Field(..., description="Error message")


class ErrorResponse(BaseModel):
    """Standard error response format"""

    error: str = Field(..., description="Error type or category")
    message: str = Field(..., description="Human-readable error message")
    details: list[ErrorDetail] | dict[str, Any] | None = Field(
        default=None, description="Additional error details"
    )

    model_config = {"json_schema_extra": {"example": {
        "error": "Validation Error",
        "message": "Request validation failed",
        "details": [{"field": "email", "message": "Invalid email format"}],
    }}}
