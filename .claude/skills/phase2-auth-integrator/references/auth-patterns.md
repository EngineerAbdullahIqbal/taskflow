# Authentication Implementation Patterns

## JWT Token Strategy

**Token Types**:
- **Access Token**: Short-lived (15 minutes), used for API requests
- **Refresh Token**: Long-lived (7 days), used to obtain new access tokens

**Token Structure**:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1640995200,
  "iat": 1640994300,
  "type": "access"
}
```

**Storage**:
- Access Token: Memory (React state/context)
- Refresh Token: httpOnly cookie (secure, not accessible to JS)

## Session Management Patterns

### Pattern 1: Automatic Token Refresh

```typescript
// Frontend: Axios interceptor for automatic refresh
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response.status === 401 && !error.config._retry) {
      error.config._retry = true
      const newToken = await refreshAccessToken()
      error.config.headers.Authorization = `Bearer ${newToken}`
      return api.request(error.config)
    }
    return Promise.reject(error)
  }
)
```

### Pattern 2: Token Expiration Check

```python
# Backend: Middleware to verify token expiration
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(401, "Token expired")
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

## Better Auth Configuration

**Backend (FastAPI)**:
```python
from better_auth import BetterAuth
from better_auth.plugins import JWTPlugin

auth = BetterAuth(
    secret=os.getenv("BETTER_AUTH_SECRET"),
    plugins=[
        JWTPlugin(
            access_token_expire_minutes=15,
            refresh_token_expire_days=7,
            algorithm="HS256"
        )
    ]
)
```

**Frontend (Next.js)**:
```typescript
import { createAuthClient } from "@better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  credentials: "include", // Send cookies
})

export const { useSession, signIn, signOut, signUp } = authClient
```

## Password Reset Flow (Optional Phase 3)

1. User requests reset → Generate reset token → Send email
2. User clicks link → Verify token → Show reset form
3. User submits new password → Hash password → Update database → Invalidate token
