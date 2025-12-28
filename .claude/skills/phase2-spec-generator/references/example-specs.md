# Example Feature Specifications

This file provides example specifications for common Phase 2 features to serve as reference templates.

---

## Example 1: User Authentication Feature

```markdown
# Feature: User Authentication

## Product Vision

**Problem Statement**: Users need secure access to their personal task data without sharing it with others.

**Solution Overview**: Implement Better Auth with JWT-based authentication, allowing users to sign up, log in, and access their own tasks securely.

**Success Metrics**:
- 95% of new users successfully complete signup
- Average login time < 3 seconds
- Zero unauthorized data access incidents

## User Stories

### Story 1: User Signup
**As a** new user
**I want** to create an account with email and password
**So that** I can start managing my tasks

**Acceptance Criteria**:
- [ ] User can enter email and password on signup form
- [ ] Email must be valid format (validated client and server-side)
- [ ] Password must be ≥8 characters with uppercase, lowercase, number, symbol
- [ ] User receives welcome email after successful signup
- [ ] User is automatically logged in after signup
- [ ] Duplicate email addresses are rejected with clear error message

### Story 2: User Login
**As a** returning user
**I want** to log in with my credentials
**So that** I can access my tasks

**Acceptance Criteria**:
- [ ] User can enter email and password on login form
- [ ] Successful login redirects to dashboard
- [ ] Invalid credentials show friendly error message
- [ ] Failed login attempts are rate-limited (max 5 per 15 minutes)
- [ ] Session persists across browser refreshes
- [ ] "Remember me" option extends session to 7 days

### Story 3: User Logout
**As a** logged-in user
**I want** to log out securely
**So that** others cannot access my tasks on shared devices

**Acceptance Criteria**:
- [ ] Logout button visible in navigation
- [ ] Clicking logout clears session and redirects to login
- [ ] JWT tokens are invalidated server-side
- [ ] Protected routes redirect to login after logout

## Technical Stack

**Frontend**:
- Next.js 16+ (App Router) - Auth routes in `app/(auth)/`
- Better Auth React hooks - `useSession()`, `useSignIn()`, `useSignUp()`
- shadcn/ui components - Form, Input, Button, Card
- Tailwind CSS - Responsive auth layouts

**Backend**:
- FastAPI routes - `/api/auth/signup`, `/api/auth/login`, `/api/auth/logout`
- Better Auth JWT plugin - Token generation and verification
- SQLModel User model - User storage with password hashing
- bcrypt - Password hashing (cost factor 12)

**Context7 Verification Notes**:
- Better Auth v1.2.0 supports JWT plugin with refresh tokens
- Next.js 16 middleware can intercept auth requests
- FastAPI Depends() pattern recommended for JWT verification
- SQLModel relationships support user → tasks foreign key

## UI/UX Requirements

### Wireframes/Mockups
- Login page: Centered card with email/password inputs, "Remember me" checkbox, login button, "Sign up" link
- Signup page: Similar layout with password confirmation, terms acceptance checkbox
- Error states: Red border on invalid inputs, error message below field

### Component Inventory
- **AuthLayout** - Centered container with branding
- **LoginForm** - Email/password inputs, submit button, validation
- **SignupForm** - Email/password/confirm inputs, terms checkbox, submit button
- **AuthError** - Toast notification for auth errors

### User Flows
1. **Signup flow**: Land on signup → Enter email/password → Accept terms → Submit → Welcome email → Redirect to dashboard
2. **Login flow**: Land on login → Enter credentials → Submit → Redirect to dashboard
3. **Error flow**: Invalid input → Show field error → Fix → Resubmit

### Responsive Design
- Mobile (< 640px): Full-width form, stacked labels
- Tablet (640px - 1024px): Max-width 600px centered
- Desktop (> 1024px): Max-width 400px centered with background image

### Accessibility (WCAG 2.1 AA)
- [ ] Form labels properly associated with inputs
- [ ] Keyboard navigation: Tab through fields, Enter to submit
- [ ] Screen reader announces errors clearly
- [ ] Color contrast 4.5:1 for all text
- [ ] Focus indicators on all interactive elements
- [ ] Password visibility toggle button accessible

## API Contracts

### Endpoint 1: POST /api/auth/signup

**Request**:
```typescript
interface SignupRequest {
  email: string        // Valid email format
  password: string     // ≥8 chars, uppercase, lowercase, number, symbol
  name: string         // 1-100 characters
}
```

**Response (201)**:
```typescript
interface SignupResponse {
  user: {
    id: string
    email: string
    name: string
  }
  access_token: string
  refresh_token: string
}
```

**Error Responses**:
- `400 Bad Request`: Invalid email format or weak password
- `409 Conflict`: Email already exists

**Authentication**: None (public endpoint)

### Endpoint 2: POST /api/auth/login

**Request**:
```typescript
interface LoginRequest {
  email: string
  password: string
  remember_me?: boolean
}
```

**Response (200)**:
```typescript
interface LoginResponse {
  user: {
    id: string
    email: string
    name: string
  }
  access_token: string
  refresh_token: string
}
```

**Error Responses**:
- `400 Bad Request`: Missing email or password
- `401 Unauthorized`: Invalid credentials
- `429 Too Many Requests`: Rate limit exceeded

**Authentication**: None (public endpoint)

### Endpoint 3: POST /api/auth/logout

**Request**: Empty body

**Response (204)**: No content

**Error Responses**:
- `401 Unauthorized`: No valid token provided

**Authentication**: Requires JWT token in Authorization header

## Database Schema

### Table: users

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

**Indexes**:
- `email` (unique, for login lookups)

**Migrations**:
- Migration: `20251227_create_users_table.py`
- Includes password hashing function
- Alembic upgrade/downgrade required

## Security Considerations

### Authentication & Authorization
- [ ] Passwords hashed with bcrypt (cost factor 12)
- [ ] JWT tokens signed with HS256 and secret from environment
- [ ] Refresh tokens rotate on use
- [ ] Session expires after 15 minutes (access token)
- [ ] Remember me extends refresh token to 7 days

### Input Validation
- [ ] Email validated with regex (client and server)
- [ ] Password strength validated (≥8 chars, mixed case, number, symbol)
- [ ] SQL injection prevented via SQLModel parameterized queries
- [ ] XSS prevented by sanitizing name field

### Data Protection
- [ ] Passwords never logged or returned in API responses
- [ ] JWT secret stored in environment variable (min 32 chars)
- [ ] HTTPS only in production
- [ ] Cookies set with httpOnly and Secure flags

## Performance Requirements

### Frontend
- [ ] Login page load < 1s
- [ ] Form submission < 500ms
- [ ] Lighthouse score ≥90
- [ ] No layout shift during loading

### Backend
- [ ] Signup endpoint < 300ms (includes bcrypt hashing)
- [ ] Login endpoint < 200ms
- [ ] JWT verification < 50ms

### Caching Strategy
- Session data cached in-memory for 15 minutes

## Testing Strategy

### Unit Tests (≥85% coverage)
- [ ] Frontend: LoginForm validation, SignupForm validation
- [ ] Backend: Password hashing, JWT generation/verification, User model validation

### Integration Tests
- [ ] Signup flow: Valid data returns 201 with tokens
- [ ] Signup flow: Duplicate email returns 409
- [ ] Login flow: Valid credentials return 200 with tokens
- [ ] Login flow: Invalid credentials return 401
- [ ] Logout flow: Valid token returns 204

### E2E Tests (Playwright)
- [ ] Complete signup flow: Form fill → Submit → Redirect to dashboard
- [ ] Complete login flow: Form fill → Submit → Redirect to dashboard
- [ ] Error handling: Invalid email → Show error → Fix → Success

## Dependencies

**New NPM Packages**:
- @better-auth/react@^1.2.0 - React hooks for Better Auth
- bcryptjs@^2.4.3 - Password hashing (client-side validation)

**New Python Packages**:
- better-auth==1.2.0 - Authentication library
- bcrypt==4.1.2 - Password hashing
- python-jose==3.3.0 - JWT encoding/decoding

## Deployment Considerations

- [ ] Environment variable `BETTER_AUTH_SECRET` (32+ char random string)
- [ ] Environment variable `FRONTEND_URL` for CORS
- [ ] Database migration for users table tested
- [ ] Email service configured (Resend API key)
- [ ] Rollback plan: Revert migration if signup fails

## Out of Scope (Phase 2)

- Social login (Google, GitHub)
- Two-factor authentication
- Password reset via email
- Account deletion

## Open Questions

1. Should we require email verification before allowing login?
2. What should the lockout duration be after 5 failed attempts?

## Approval

- [ ] Product Owner: _______________
- [ ] Tech Lead: _______________
- [ ] Date: _______________
```

---

## Example 2: Task Dashboard Feature

```markdown
# Feature: Task Dashboard

## Product Vision

**Problem Statement**: Users need a quick overview of their tasks with filtering and sorting capabilities.

**Solution Overview**: A responsive dashboard showing task cards with status indicators, filters (all/pending/completed), and sorting options (date/title).

**Success Metrics**:
- Users can view all tasks in < 2 seconds
- 80% of users use filters at least once per session
- Mobile responsiveness works on 95% of devices

## User Stories

### Story 1: View Task List
**As a** logged-in user
**I want** to see all my tasks in a list
**So that** I can quickly assess what needs to be done

**Acceptance Criteria**:
- [ ] Dashboard loads within 2 seconds
- [ ] Tasks displayed as cards with title, description, status
- [ ] Empty state shown when no tasks exist
- [ ] Loading skeleton shown while fetching
- [ ] Tasks paginated (20 per page)

[Continue with remaining stories, technical stack, UI/UX, API, etc.]
```

---

## Common Specification Patterns

### Pattern 1: CRUD Feature
- User stories for Create, Read (list + detail), Update, Delete
- API endpoints following RESTful conventions
- Database schema with proper indexes
- Form validation on both client and server

### Pattern 2: Authentication Feature
- Signup, Login, Logout user stories
- JWT token management
- Password security (hashing, strength requirements)
- Rate limiting on auth endpoints

### Pattern 3: Dashboard/List Feature
- Pagination, filtering, sorting
- Empty states and loading states
- Responsive grid/list layouts
- Real-time updates (optional)

### Pattern 4: Settings/Profile Feature
- User preferences management
- Form with validation
- Optimistic UI updates
- Rollback on failure

---

Use these examples as templates when creating new feature specifications. Adapt sections based on feature complexity and requirements.
