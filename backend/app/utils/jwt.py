"""JWT token generation and refresh utilities"""

from datetime import datetime, timedelta, timezone

from jose import jwt

from app.config import settings


def create_access_token(user_id: int) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: User's database ID

    Returns:
        str: Encoded JWT access token

    Example:
        >>> token = create_access_token(user_id=123)
        >>> len(token) > 0
        True
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
    }

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(user_id: int) -> str:
    """
    Create a JWT refresh token for a user.

    Args:
        user_id: User's database ID

    Returns:
        str: Encoded JWT refresh token

    Example:
        >>> token = create_refresh_token(user_id=123)
        >>> len(token) > 0
        True
    """
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
    }

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> dict[str, any]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token to verify

    Returns:
        dict: Decoded token payload

    Raises:
        JWTError: If token is invalid or expired

    Example:
        >>> token = create_access_token(user_id=123)
        >>> payload = verify_token(token)
        >>> payload["sub"]
        '123'
    """
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return payload
