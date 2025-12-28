"""Authentication request/response schemas"""

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """User signup request schema"""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password (8+ chars, upper, lower, number, special)",
    )
    name: str = Field(..., min_length=1, max_length=255, description="User full name")


class LoginRequest(BaseModel):
    """User login request schema"""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """JWT token response schema"""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")


class UserResponse(BaseModel):
    """User profile response schema"""

    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    created_at: str = Field(..., description="Account creation timestamp")
    updated_at: str = Field(..., description="Account update timestamp")
