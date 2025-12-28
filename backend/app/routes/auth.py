"""Authentication endpoints"""

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.middleware.auth import CurrentUserId
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.utils.database import SessionDep

router = APIRouter()

# Rate limiting storage (in-memory, use Redis in production)
_rate_limit_storage: dict[str, list[datetime]] = defaultdict(list)
_RATE_LIMIT_ATTEMPTS = 5
_RATE_LIMIT_WINDOW = timedelta(minutes=15)


def _check_rate_limit(ip_address: str) -> None:
    """
    Check if request is within rate limit.

    Args:
        ip_address: Client IP address

    Raises:
        HTTPException: 429 if rate limit exceeded
    """
    now = datetime.now(timezone.utc)
    cutoff = now - _RATE_LIMIT_WINDOW

    # Clean old attempts
    _rate_limit_storage[ip_address] = [
        attempt for attempt in _rate_limit_storage[ip_address] if attempt > cutoff
    ]

    # Check limit
    if len(_rate_limit_storage[ip_address]) >= _RATE_LIMIT_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many attempts. Try again in {_RATE_LIMIT_WINDOW.seconds // 60} minutes",
        )

    # Record attempt
    _rate_limit_storage[ip_address].append(now)


@router.post("/signup", response_model=dict[str, UserResponse | TokenResponse], status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    session: SessionDep,
    http_request: Request,
) -> dict[str, UserResponse | TokenResponse]:
    """
    Create a new user account.

    Args:
        request: SignupRequest with email, password, name
        session: Database session
        http_request: FastAPI request for rate limiting

    Returns:
        Dictionary with user and tokens

    Raises:
        HTTPException: 400 if email exists or password weak, 429 if rate limited

    Example:
        POST /auth/signup
        {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "name": "John Doe"
        }

        Response:
        {
            "user": {
                "id": 1,
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2025-12-28T12:00:00Z",
                "updated_at": "2025-12-28T12:00:00Z"
            },
            "tokens": {
                "access_token": "eyJ...",
                "refresh_token": "eyJ...",
                "token_type": "bearer"
            }
        }
    """
    # Apply rate limiting
    client_ip = http_request.client.host if http_request.client else "unknown"
    _check_rate_limit(client_ip)

    # Create user
    auth_service = AuthService(session)
    user, tokens = await auth_service.signup(request)

    return {"user": user, "tokens": tokens}


@router.post("/login", response_model=dict[str, UserResponse | TokenResponse])
async def login(
    request: LoginRequest,
    session: SessionDep,
    http_request: Request,
) -> dict[str, UserResponse | TokenResponse]:
    """
    Authenticate user with email/password.

    Args:
        request: LoginRequest with email, password
        session: Database session
        http_request: FastAPI request for rate limiting

    Returns:
        Dictionary with user and tokens

    Raises:
        HTTPException: 401 if credentials invalid, 429 if rate limited

    Example:
        POST /auth/login
        {
            "email": "user@example.com",
            "password": "SecurePass123!"
        }

        Response:
        {
            "user": {
                "id": 1,
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2025-12-28T12:00:00Z",
                "updated_at": "2025-12-28T12:00:00Z"
            },
            "tokens": {
                "access_token": "eyJ...",
                "refresh_token": "eyJ...",
                "token_type": "bearer"
            }
        }
    """
    # Apply rate limiting
    client_ip = http_request.client.host if http_request.client else "unknown"
    _check_rate_limit(client_ip)

    # Authenticate user
    auth_service = AuthService(session)
    user, tokens = await auth_service.login(request)

    return {"user": user, "tokens": tokens}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    user_id: CurrentUserId,
    session: SessionDep,
) -> None:
    """
    Logout user (token invalidation placeholder).

    Args:
        user_id: Current authenticated user ID
        session: Database session

    Returns:
        204 No Content

    Note:
        Token invalidation is not fully implemented.
        In production, use Redis blacklist or short-lived tokens.

    Example:
        POST /auth/logout
        Headers: Authorization: Bearer <token>

        Response: 204 No Content
    """
    auth_service = AuthService(session)
    await auth_service.logout(user_id)
