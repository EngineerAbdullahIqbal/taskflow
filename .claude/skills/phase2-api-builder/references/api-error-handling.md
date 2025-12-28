# API Error Handling Standards

## Constitution Error Response Format

**All errors MUST follow this format:**

```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE"
}
```

## Common HTTP Status Codes

| Status | Use Case | Example |
|--------|----------|---------|
| 200 | Successful GET/PATCH | Task retrieved/updated |
| 201 | Successful POST (created) | Task created |
| 204 | Successful DELETE (no content) | Task deleted |
| 400 | Bad request (validation failed) | Invalid input data |
| 401 | Unauthorized (not authenticated) | Missing/invalid JWT token |
| 403 | Forbidden (authenticated but not authorized) | User cannot access resource |
| 404 | Resource not found | Task ID doesn't exist |
| 409 | Conflict (duplicate) | Email already exists |
| 422 | Unprocessable entity (Pydantic validation) | Field validation failed |
| 429 | Too many requests (rate limit) | Max login attempts exceeded |
| 500 | Internal server error | Database connection failed |

## Error Response Patterns

### Pattern 1: Resource Not Found (404)

```python
from fastapi import HTTPException

@router.get("/api/tasks/{task_id}")
async def get_task(task_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_session)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
            headers={"error_code": "TASK_NOT_FOUND"}
        )

    # Verify ownership (403 if not owner)
    if task.user_id != user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this task",
            headers={"error_code": "FORBIDDEN"}
        )

    return task
```

**Client receives:**
```json
{
  "detail": "Task not found",
  "error_code": "TASK_NOT_FOUND"
}
```

### Pattern 2: Validation Errors (400/422)

**Pydantic Validation** (automatic):
```python
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

    @field_validator('title')
    def validate_title(cls, v: str) -> str:
        if len(v) < 1 or len(v) > 200:
            raise ValueError("Title must be 1-200 characters")
        return v.strip()
```

**Client receives (auto-formatted by FastAPI):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "title"],
      "msg": "Title must be 1-200 characters",
      "input": ""
    }
  ]
}
```

**Custom Validation Error**:
```python
@router.post("/api/tasks")
async def create_task(task: TaskCreate, user: dict = Depends(get_current_user)):
    # Business logic validation
    if len(task.title.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty",
            headers={"error_code": "INVALID_TITLE"}
        )
```

### Pattern 3: Duplicate Resource (409)

```python
@router.post("/api/auth/signup")
async def signup(request: SignupRequest, db: Session = Depends(get_session)):
    existing_user = db.exec(select(User).where(User.email == request.email)).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
            headers={"error_code": "EMAIL_ALREADY_EXISTS"}
        )

    # Create user
    user = User(email=request.email, ...)
    db.add(user)
    db.commit()
    return user
```

### Pattern 4: Authentication Errors (401)

```python
# Missing token
@router.get("/api/tasks")
async def get_tasks(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"error_code": "AUTH_REQUIRED"}
        )

# Invalid token
@router.get("/api/tasks")
async def get_tasks(user: dict = Depends(get_current_user)):
    # get_current_user raises 401 if token invalid
    pass
```

### Pattern 5: Rate Limiting (429)

```python
from collections import defaultdict
from datetime import datetime, timedelta

failed_attempts = defaultdict(list)

@router.post("/api/auth/login")
async def login(request: LoginRequest):
    email = request.email
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=15)

    # Remove old attempts
    failed_attempts[email] = [t for t in failed_attempts[email] if t > cutoff]

    if len(failed_attempts[email]) >= 5:
        raise HTTPException(
            status_code=429,
            detail="Too many failed login attempts. Try again in 15 minutes.",
            headers={"error_code": "RATE_LIMIT_EXCEEDED"}
        )

    # Verify credentials
    user = authenticate(request.email, request.password)
    if not user:
        failed_attempts[email].append(now)
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"error_code": "INVALID_CREDENTIALS"}
        )

    # Success: clear failed attempts
    failed_attempts.pop(email, None)
    return generate_tokens(user)
```

### Pattern 6: Internal Server Errors (500)

**Global Exception Handler**:

```python
# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions and return 500."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # NEVER expose stack traces in production
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR"
        }
    )
```

## Error Code Registry

**Maintain a central registry of error codes:**

```python
# backend/app/errors.py
class ErrorCode:
    # Authentication (1xxx)
    AUTH_REQUIRED = "AUTH_REQUIRED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

    # Resources (2xxx)
    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"

    # Validation (3xxx)
    INVALID_TITLE = "INVALID_TITLE"
    INVALID_EMAIL = "INVALID_EMAIL"

    # Permissions (4xxx)
    FORBIDDEN = "FORBIDDEN"

    # Conflicts (5xxx)
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    TASK_ALREADY_COMPLETED = "TASK_ALREADY_COMPLETED"

# Usage
raise HTTPException(
    status_code=404,
    detail="Task not found",
    headers={"error_code": ErrorCode.TASK_NOT_FOUND}
)
```

## Frontend Error Handling

**TypeScript Error Types**:

```typescript
// frontend/lib/api/types.ts
export interface ApiError {
  detail: string
  error_code?: string
}

export class ApiException extends Error {
  constructor(
    public status: number,
    public error: ApiError
  ) {
    super(error.detail)
    this.name = 'ApiException'
  }
}

// frontend/lib/api/client.ts
async function apiRequest<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options)

  if (!response.ok) {
    const error: ApiError = await response.json()
    throw new ApiException(response.status, error)
  }

  return response.json()
}

// Usage in component
try {
  const task = await apiRequest<Task>('/api/tasks/123')
} catch (error) {
  if (error instanceof ApiException) {
    if (error.error.error_code === 'TASK_NOT_FOUND') {
      toast.error('Task not found')
    } else if (error.status === 401) {
      router.push('/login')
    } else {
      toast.error(error.error.detail)
    }
  }
}
```

## Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

@router.post("/api/tasks")
async def create_task(task: TaskCreate, user: dict = Depends(get_current_user)):
    try:
        # Log important events
        logger.info(f"User {user['id']} creating task: {task.title}")

        new_task = Task(**task.dict(), user_id=user["id"])
        db.add(new_task)
        db.commit()

        logger.info(f"Task {new_task.id} created successfully")
        return new_task

    except Exception as e:
        # Log errors with context
        logger.error(
            f"Failed to create task for user {user['id']}: {e}",
            exc_info=True,
            extra={"user_id": user["id"], "task_title": task.title}
        )
        raise

# NEVER log sensitive data
# ❌ logger.info(f"User password: {password}")
# ❌ logger.info(f"JWT token: {token}")
```

## Testing Error Responses

```python
# backend/tests/routes/test_tasks.py
def test_get_task_not_found(client, auth_headers):
    response = client.get("/api/tasks/999", headers=auth_headers)

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task not found"
    assert data["error_code"] == "TASK_NOT_FOUND"

def test_create_task_unauthorized(client):
    response = client.post("/api/tasks", json={"title": "Test"})

    assert response.status_code == 401
    data = response.json()
    assert data["error_code"] == "AUTH_REQUIRED"

def test_create_task_invalid_title(client, auth_headers):
    response = client.post(
        "/api/tasks",
        json={"title": ""},  # Empty title
        headers=auth_headers
    )

    assert response.status_code == 400 or response.status_code == 422
```
