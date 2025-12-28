"""FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.middleware.error_handler import add_exception_handlers

# Create FastAPI app
app = FastAPI(
    title="TaskFlow API",
    description="Task and habit tracking API with reminders",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
add_exception_handlers(app)

# Import and include routers
from app.routes import auth, health

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# TODO: Uncomment as routes are implemented
# from app.routes import tasks, categories, notifications, preferences
# app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
# app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
# app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
# app.include_router(preferences.router, prefix="/api/preferences", tags=["preferences"])


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "message": "TaskFlow API - Phase 2",
        "version": "2.0.0",
        "docs": "/api/docs",
    }
