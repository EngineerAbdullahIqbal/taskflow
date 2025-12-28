---
name: phase2-auth-integrator
description: Integrate Better Auth with JWT authentication into TaskFlow Phase 2 applications. Use when implementing authentication systems including signup, login, logout, protected routes, session management, and JWT token handling. Triggers on "integrate auth", "setup authentication", "add better auth", "implement JWT auth", or "/phase2-auth-integrator". Requires approved specification with authentication requirements.
---

# Phase 2 Auth Integrator

Integrate Better Auth with JWT authentication into TaskFlow Phase 2 full-stack applications.

## Workflow

### 1. Verify Authentication Requirements

Check that approved specification includes:
- Authentication user stories (signup, login, logout)
- Password requirements and validation rules
- Session duration and refresh token strategy
- Protected route requirements

If missing, suggest running `/phase2-spec-generator` with auth feature.

### 2. Fetch Better Auth Documentation (Context7)

**Context7 Query Process**:
1. Use `mcp__context7__resolve-library-id` with query: "better-auth"
2. Use `mcp__context7__get-library-docs` with `mode='code'` to fetch:
   - JWT plugin configuration
   - Session management patterns
   - Password hashing setup (bcrypt)
   - Middleware integration for Next.js and FastAPI
   - Token refresh strategies

3. Document library version and patterns used

### 3. Backend Integration (FastAPI)

**Generate Auth Service** (`backend/app/services/auth_service.py`):
- Password hashing with bcrypt (cost factor 12)
- JWT token generation (access + refresh)
- User validation and session management
- Token verification and refresh logic

**Generate Auth Routes** (`backend/app/routes/auth.py`):
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User authentication
- `POST /api/auth/logout` - Session termination
- `POST /api/auth/refresh` - Token refresh
- `GET /api/auth/me` - Current user info

**Generate Auth Middleware** (`backend/app/middleware/auth.py`):
- JWT token extraction from Authorization header
- Token validation and expiration checking
- User context injection into request
- Protected route decorator

### 4. Database Models (SQLModel)

**Generate User Model** (`backend/app/models/user.py`):
```python
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    email_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Generate Migration**: `backend/app/migrations/<timestamp>_create_users_table.py`

### 5. Frontend Integration (Next.js + React)

**Generate Auth Context** (`frontend/lib/auth-context.tsx`):
- Better Auth React hooks setup
- Session state management
- Token storage and refresh logic

**Generate Auth API Client** (`frontend/lib/api/auth.ts`):
- Type-safe auth API calls
- Error handling for auth failures
- Token injection into requests

**Generate Auth Components**:
- `frontend/components/features/auth/LoginForm.tsx`
- `frontend/components/features/auth/SignupForm.tsx`
- `frontend/components/features/auth/AuthLayout.tsx`
- `frontend/components/features/auth/ProtectedRoute.tsx`

**Generate Auth Routes**:
- `frontend/app/(auth)/login/page.tsx`
- `frontend/app/(auth)/signup/page.tsx`

### 6. Environment Configuration

**Generate `.env.example`**:
```bash
# Backend
BETTER_AUTH_SECRET=<32-char-random-string>
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Document secret generation: `openssl rand -hex 32`

### 7. Testing Integration

**Generate Backend Tests**:
- `backend/tests/services/test_auth_service.py` - Password hashing, JWT generation
- `backend/tests/routes/test_auth.py` - Signup, login, logout, refresh flows
- `backend/tests/middleware/test_auth.py` - Token validation, protected routes

**Generate Frontend Tests**:
- `frontend/__tests__/components/auth/LoginForm.test.tsx` - Form validation
- `frontend/__tests__/components/auth/SignupForm.test.tsx` - Signup flow
- `frontend/__tests__/lib/api/auth.test.ts` - API client tests

**Generate E2E Tests**:
- `e2e/auth.spec.ts` - Complete signup → login → protected route flow

### 8. Validation & Next Steps

**Validation Checklist**:
- [ ] All auth routes generated (signup, login, logout, refresh)
- [ ] User model includes password_hash (never plaintext)
- [ ] JWT tokens use environment secret
- [ ] Protected routes middleware implemented
- [ ] Auth context provides session state
- [ ] Login/signup forms validate inputs
- [ ] Tests cover auth flows (≥85% coverage)
- [ ] Environment variables documented

**Next Steps**:
Inform user: "✅ Better Auth integration complete. Review generated files, then run `/quality-gate` to validate auth implementation before deploying."

## Context7 Library Reference

| Library | ID | Integration Details |
|---------|-----|---------------------|
| Better Auth | `/better-auth/better-auth` | JWT plugin, session config, middleware |
| bcrypt | Search "bcrypt python" | Password hashing (cost factor 12) |
| FastAPI Auth | `/fastapi/fastapi` | Dependency injection for auth, OAuth2 flows |

## References

See `references/` for:
- `auth-patterns.md` - JWT implementation patterns, session strategies
- `protected-routes.md` - Middleware examples for frontend and backend
- `password-security.md` - Hashing standards, validation rules
