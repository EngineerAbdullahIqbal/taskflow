"""Database configuration and session management"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from app.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    future=True,
)

# Create async session factory
async_session_maker = sessionmaker(
    engine, class_=SQLModelAsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.

    Yields:
        AsyncSession: Database session

    Example:
        @app.get("/users")
        async def get_users(session: Annotated[AsyncSession, Depends(get_session)]):
            result = await session.execute(select(User))
            return result.scalars().all()
    """
    async with async_session_maker() as session:
        yield session


# Type alias for session dependency
SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def init_db() -> None:
    """
    Initialize database tables.

    Note: In production, use Alembic migrations instead.
    This is only for development/testing.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
