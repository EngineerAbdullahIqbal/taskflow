# FastAPI Implementation Patterns

## Dependency Injection

**Pattern 1: Database Session Injection**

```python
# backend/app/database.py
from sqlmodel import Session, create_engine

engine = create_engine("postgresql://...")

def get_session():
    """Provide database session to routes."""
    with Session(engine) as session:
        yield session

# Usage in route
@router.get("/api/tasks")
async def get_tasks(db: Session = Depends(get_session)):
    tasks = db.exec(select(Task)).all()
    return tasks
```

**Pattern 2: Current User Injection**

```python
# backend/app/middleware/auth.py
from fastapi import Depends, HTTPException, Header
from typing import Annotated

async def get_current_user(
    authorization: Annotated[str | None, Header()] = None
) -> dict:
    """Extract and verify JWT token."""
    if not authorization:
        raise HTTPException(401, "Authentication required")

    token = authorization.replace("Bearer ", "")
    payload = verify_jwt(token)
    return {"id": payload["sub"], "email": payload["email"]}

# Usage in route (chained dependencies)
@router.get("/api/tasks")
async def get_tasks(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return db.query(Task).filter(Task.user_id == user["id"]).all()
```

**Pattern 3: Service Injection**

```python
# backend/app/dependencies.py
from app.services.task_service import TaskService

def get_task_service(db: Session = Depends(get_session)) -> TaskService:
    """Provide task service instance."""
    return TaskService(db)

# Usage in route
@router.get("/api/tasks")
async def get_tasks(
    user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return service.get_all(user["id"])
```

## Error Handling

**Pattern 1: Custom Exception Handler**

```python
# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Standardized error response format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.headers.get("error_code") if exc.headers else None
        }
    )

# Usage in route
@router.get("/api/tasks/{task_id}")
async def get_task(task_id: int):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
            headers={"error_code": "TASK_NOT_FOUND"}
        )
    return task
```

**Pattern 2: Validation Error Handler**

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Format Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=400,
        content={"detail": "Validation failed", "errors": errors}
    )
```

## Pagination

**Pattern 1: Query Parameter Pagination**

```python
from fastapi import Query

@router.get("/api/tasks")
async def get_tasks(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max items to return"),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """List tasks with pagination."""
    statement = (
        select(Task)
        .where(Task.user_id == user["id"])
        .offset(skip)
        .limit(limit)
    )
    tasks = db.exec(statement).all()

    # Optional: Include total count
    total = db.exec(select(func.count(Task.id)).where(Task.user_id == user["id"])).one()

    return {
        "items": tasks,
        "total": total,
        "skip": skip,
        "limit": limit
    }
```

**Pattern 2: Cursor-Based Pagination (for large datasets)**

```python
@router.get("/api/tasks")
async def get_tasks(
    cursor: int | None = Query(None, description="Last seen task ID"),
    limit: int = Query(100, ge=1, le=100),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Cursor-based pagination (better for real-time feeds)."""
    statement = select(Task).where(Task.user_id == user["id"])

    if cursor:
        statement = statement.where(Task.id < cursor)

    statement = statement.order_by(Task.id.desc()).limit(limit)
    tasks = db.exec(statement).all()

    next_cursor = tasks[-1].id if tasks else None

    return {
        "items": tasks,
        "next_cursor": next_cursor
    }
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email_notification(user_email: str, task_title: str):
    """Background task to send email (don't block response)."""
    # Send email logic
    pass

@router.post("/api/tasks", status_code=201)
async def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create task and send notification in background."""
    new_task = Task(**task.dict(), user_id=user["id"])
    db.add(new_task)
    db.commit()

    # Queue background task (non-blocking)
    background_tasks.add_task(send_email_notification, user["email"], new_task.title)

    return new_task
```

## Response Models

**Pattern: Multiple Response Models**

```python
from pydantic import BaseModel

class TaskSummary(BaseModel):
    """Minimal task info for list views."""
    id: int
    title: str
    completed: bool

class TaskDetail(BaseModel):
    """Full task info for detail views."""
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: str

@router.get("/api/tasks", response_model=list[TaskSummary])
async def get_tasks():
    """Returns summary only (faster)."""
    pass

@router.get("/api/tasks/{task_id}", response_model=TaskDetail)
async def get_task(task_id: int):
    """Returns full details."""
    pass
```

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        "https://taskflow.com"    # Production
    ],
    allow_credentials=True,       # Allow cookies
    allow_methods=["*"],          # Allow all HTTP methods
    allow_headers=["*"],          # Allow all headers
)
```
