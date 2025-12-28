"""Authentication service layer"""

import re
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User
from app.models.notification_preference import NotificationPreference
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, UserResponse
from app.utils.jwt import create_access_token, create_refresh_token
from app.utils.security import hash_password, verify_password


class AuthService:
    """Service for user authentication operations"""

    def __init__(self, session: AsyncSession):
        """Initialize with async database session"""
        self.session = session

    async def signup(self, request: SignupRequest) -> tuple[UserResponse, TokenResponse]:
        """
        Create a new user account with email/password.

        Args:
            request: SignupRequest with email, password, name

        Returns:
            Tuple of (UserResponse, TokenResponse)

        Raises:
            HTTPException: 400 if email already exists or password too weak
        """
        # Validate password strength
        self._validate_password_strength(request.password)

        # Check if email already exists
        existing_user = await self._get_user_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Hash password
        password_hash = hash_password(request.password)

        # Create user (use naive datetime for TIMESTAMP WITHOUT TIME ZONE)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        user = User(
            email=request.email,
            name=request.name,
            password_hash=password_hash,
            created_at=now,
            updated_at=now,
        )

        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create default notification preferences (use naive datetime)
        now_pref = datetime.now(timezone.utc).replace(tzinfo=None)
        notification_pref = NotificationPreference(
            user_id=user.id,
            reminder_email=user.email,
            email_notifications_enabled=True,
            browser_notifications_enabled=True,
            created_at=now_pref,
            updated_at=now_pref,
        )
        self.session.add(notification_pref)
        await self.session.commit()

        # Generate tokens
        tokens = self._generate_tokens(user.id)

        # Build user response
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        )

        return user_response, tokens

    async def login(self, request: LoginRequest) -> tuple[UserResponse, TokenResponse]:
        """
        Authenticate user with email/password.

        Args:
            request: LoginRequest with email, password

        Returns:
            Tuple of (UserResponse, TokenResponse)

        Raises:
            HTTPException: 401 if credentials invalid
        """
        # Get user by email
        user = await self._get_user_by_email(request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Verify password
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Generate tokens
        tokens = self._generate_tokens(user.id)

        # Build user response
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        )

        return user_response, tokens

    async def logout(self, user_id: int) -> None:
        """
        Logout user (placeholder for token invalidation).

        Args:
            user_id: User ID to logout

        Note:
            Token invalidation is not fully implemented.
            In production, use Redis blacklist or short-lived tokens.
        """
        # Placeholder - actual token invalidation would require Redis or database
        pass

    async def _get_user_by_email(self, email: str) -> User | None:
        """Get user by email address"""
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()

    def _generate_tokens(self, user_id: int) -> TokenResponse:
        """Generate access and refresh tokens for user"""
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @staticmethod
    def _validate_password_strength(password: str) -> None:
        """
        Validate password meets strength requirements.

        Requirements:
        - At least 8 characters
        - Contains uppercase letter
        - Contains lowercase letter
        - Contains digit
        - Contains special character

        Args:
            password: Password to validate

        Raises:
            HTTPException: 400 if password doesn't meet requirements
        """
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters",
            )

        if not re.search(r"[A-Z]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase letter",
            )

        if not re.search(r"[a-z]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one lowercase letter",
            )

        if not re.search(r"\d", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one digit",
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one special character",
            )
