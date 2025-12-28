---
name: phase2-api-builder
description: Generate complete FastAPI CRUD APIs with SQLModel models, Pydantic schemas, service layer, routes, and tests for TaskFlow Phase 2. Use when building backend API endpoints with database persistence, input validation, error handling, and authentication. Triggers on "build api", "create api", "generate routes", "build backend", or "/phase2-api-builder". Requires approved specification with API contracts defined.
---

# Phase 2 API Builder

Generate production-ready FastAPI CRUD APIs with full type safety and layered architecture.

## Workflow

### 1. Verify API Specification

Check that approved specification includes:
- API endpoint definitions (HTTP methods, paths)
- Request/response schemas (TypeScript interfaces)
- Database schema (table structure, relationships)
- Authentication requirements
- Validation rules and constraints

If missing, suggest running `/phase2-spec-generator` first.

### 2. Fetch Library Documentation (Context7)

**Context7 Query Process**:
1. Use `mcp__context7__resolve-library-id` for FastAPI and SQLModel
2. Use `mcp__context7__get-library-docs` with `mode='code'` to fetch:
   - FastAPI dependency injection patterns
   - SQLModel relationship definitions
   - Pydantic validation patterns
   - Query optimization techniques
   - Error handling best practices

3. Document library versions and patterns used

### 3. Generate Database Models (SQLModel)

**Generate Models** (`backend/app/models/<resource>.py`):
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="tasks")
```

**Generate Migration**: `backend/app/migrations/<timestamp>_create_<resource>_table.py`

### 4. Generate Pydantic Schemas

**Generate Request/Response Schemas** (`backend/app/schemas/<resource>.py`):
```python
from pydantic import BaseModel, field_validator
from datetime import datetime

# Request schemas (input validation)
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

    @field_validator('title')
    def validate_title(cls, v: str) -> str:
        if len(v) < 1 or len(v) > 200:
            raise ValueError("Title must be 1-200 characters")
        return v.strip()

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

# Response schemas (output serialization)
class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode
```

### 5. Generate Service Layer

**Generate Service** (`backend/app/services/<resource>_service.py`):
```python
from sqlmodel import Session, select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: str, skip: int = 0, limit: int = 100) -> list[Task]:
        """Get all tasks for user with pagination."""
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Task.created_at.desc())
        )
        return self.db.exec(statement).all()

    def get_by_id(self, task_id: int, user_id: str) -> Task:
        """Get task by ID, verify ownership."""
        task = self.db.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(404, "Task not found")
        return task

    def create(self, task_data: TaskCreate, user_id: str) -> Task:
        """Create new task."""
        task = Task(**task_data.model_dump(), user_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task_id: int, task_data: TaskUpdate, user_id: str) -> Task:
        """Update task, verify ownership."""
        task = self.get_by_id(task_id, user_id)
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        task.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int, user_id: str) -> None:
        """Delete task, verify ownership."""
        task = self.get_by_id(task_id, user_id)
        self.db.delete(task)
        self.db.commit()
```

### 6. Generate FastAPI Routes

**Generate Router** (`backend/app/routes/<resource>.py`):
```python
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.database import get_session
from app.middleware.auth import get_current_user
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("", response_model=list[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get all tasks for authenticated user."""
    service = TaskService(db)
    return service.get_all(user["id"], skip, limit)

@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    task: TaskCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create new task."""
    service = TaskService(db)
    return service.create(task, user["id"])

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get task by ID."""
    service = TaskService(db)
    return service.get_by_id(task_id, user["id"])

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Update task."""
    service = TaskService(db)
    return service.update(task_id, task, user["id"])

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete task."""
    service = TaskService(db)
    service.delete(task_id, user["id"])
```

**Register Router** in `backend/app/main.py`:
```python
from app.routes import task
app.include_router(task.router)
```

### 7. Generate Tests

**Generate Service Tests** (`backend/tests/services/test_<resource>_service.py`):
```python
import pytest
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate

def test_create_task(db_session, test_user):
    service = TaskService(db_session)
    task_data = TaskCreate(title="Test Task", description="Test Description")
    task = service.create(task_data, test_user.id)

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.user_id == test_user.id
    assert task.completed is False

def test_get_all_tasks(db_session, test_user, test_tasks):
    service = TaskService(db_session)
    tasks = service.get_all(test_user.id)

    assert len(tasks) == len(test_tasks)
    assert all(t.user_id == test_user.id for t in tasks)
```

**Generate Route Tests** (`backend/tests/routes/test_<resource>.py`):
```python
def test_create_task_unauthorized(client):
    response = client.post("/api/tasks", json={"title": "Test"})
    assert response.status_code == 401

def test_create_task_authorized(client, auth_headers):
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data
```

### 8. Validation & Documentation

**Validation Checklist**:
- [ ] Models follow SQLModel conventions (snake_case, proper indexes)
- [ ] Schemas validate all inputs (field_validator for constraints)
- [ ] Service layer handles ownership verification
- [ ] Routes use dependency injection (get_current_user, get_session)
- [ ] All routes return proper status codes (200, 201, 204, 404)
- [ ] Error responses follow constitution format
- [ ] Pagination implemented for list endpoints (skip, limit)
- [ ] Tests cover CRUD operations (≥85% coverage)

**Generate OpenAPI Documentation**: FastAPI auto-generates at `/docs`

**Next Steps**:
Inform user: "✅ API implementation complete. Test endpoints at http://localhost:8000/docs, then run `/quality-gate` before deploying."

## Context7 Library Reference

| Library | ID | Documentation Needed |
|---------|-----|----------------------|
| FastAPI | `/fastapi/fastapi` | Dependency injection, route organization, validation |
| SQLModel | `/tiangolo/sqlmodel` | Relationships, queries, migrations |
| Pydantic | `/pydantic/pydantic` | Validators, serialization, config |

## References

See `references/` for:
- `fastapi-patterns.md` - Dependency injection, error handling, pagination
- `sqlmodel-relationships.md` - One-to-many, many-to-many patterns
- `api-error-handling.md` - Standardized error responses
