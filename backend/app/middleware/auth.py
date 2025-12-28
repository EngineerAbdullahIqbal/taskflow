"""JWT Authentication Middleware"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings

# HTTP Bearer token extractor
security = HTTPBearer()


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> int:
    """
    Extract and verify JWT token, return user ID.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        int: User ID from token payload

    Raises:
        HTTPException: 401 if token is invalid or missing

    Example:
        @app.get("/api/tasks")
        async def get_tasks(user_id: Annotated[int, Depends(get_current_user_id)]):
            # user_id is extracted from JWT
            return {"user_id": user_id}
    """
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        # Extract user ID from payload
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        user_id = int(user_id_str)

    except (JWTError, ValueError):
        raise credentials_exception

    return user_id


# Type alias for dependency injection
CurrentUserId = Annotated[int, Depends(get_current_user_id)]
