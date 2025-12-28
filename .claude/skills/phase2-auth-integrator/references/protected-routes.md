# Protected Routes Implementation

## Backend Protected Routes (FastAPI)

### Pattern 1: Dependency Injection

```python
# backend/app/middleware/auth.py
from fastapi import Depends, HTTPException, Header
from typing import Annotated

async def get_current_user(
    authorization: Annotated[str | None, Header()] = None
) -> dict:
    """Extract and verify JWT token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid Authorization header")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"id": payload["sub"], "email": payload["email"]}
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid or expired token")

# Usage in route
@router.get("/api/tasks")
async def get_tasks(user: dict = Depends(get_current_user)):
    # user is automatically injected
    tasks = db.query(Task).filter(Task.user_id == user["id"]).all()
    return tasks
```

### Pattern 2: Route Decorator

```python
# backend/app/middleware/auth.py
from functools import wraps

def require_auth(f):
    """Decorator to protect routes requiring authentication."""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            raise HTTPException(401, "Authentication required")

        try:
            user = verify_token(token)
            return await f(*args, user=user, **kwargs)
        except Exception:
            raise HTTPException(401, "Invalid token")

    return decorated_function

# Usage
@router.post("/api/tasks")
@require_auth
async def create_task(task: TaskCreate, user: dict):
    new_task = Task(**task.dict(), user_id=user["id"])
    db.add(new_task)
    db.commit()
    return new_task
```

## Frontend Protected Routes (Next.js)

### Pattern 1: Middleware (App Router)

```typescript
// frontend/middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token')?.value

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Optionally verify token expiration
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    if (payload.exp * 1000 < Date.now()) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  } catch {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/tasks/:path*', '/settings/:path*']
}
```

### Pattern 2: Protected Route Component

```typescript
// frontend/components/features/auth/ProtectedRoute.tsx
import { useSession } from '@better-auth/react'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { session, isLoading } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !session) {
      router.push('/login')
    }
  }, [session, isLoading, router])

  if (isLoading) {
    return <div>Loading...</div>
  }

  if (!session) {
    return null
  }

  return <>{children}</>
}

// Usage in page
export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <h1>Dashboard</h1>
      {/* Protected content */}
    </ProtectedRoute>
  )
}
```

### Pattern 3: Server Component (App Router)

```typescript
// frontend/app/dashboard/page.tsx
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

async function verifyAuth() {
  const cookieStore = cookies()
  const token = cookieStore.get('access_token')?.value

  if (!token) {
    redirect('/login')
  }

  // Verify with backend
  const res = await fetch(`${process.env.API_URL}/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  })

  if (!res.ok) {
    redirect('/login')
  }

  return res.json()
}

export default async function DashboardPage() {
  const user = await verifyAuth()

  return (
    <div>
      <h1>Welcome, {user.name}</h1>
    </div>
  )
}
```

## Role-Based Access Control (Future)

```python
# backend/app/middleware/auth.py
def require_role(allowed_roles: list[str]):
    """Decorator to restrict routes by user role."""
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, user: dict, **kwargs):
            if user.get("role") not in allowed_roles:
                raise HTTPException(403, "Insufficient permissions")
            return await f(*args, user=user, **kwargs)
        return decorated_function
    return decorator

# Usage
@router.delete("/api/users/{user_id}")
@require_role(["admin"])
async def delete_user(user_id: str, user: dict = Depends(get_current_user)):
    # Only admins can delete users
    pass
```
