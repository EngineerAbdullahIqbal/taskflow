# TaskFlow Constitution - Specification Requirements

## Relevant Sections for Feature Specifications

### Product Vision & Mission (must align)

**Mission**: Build a reliable, fast, and user-friendly task management platform that helps individuals and teams stay organized without overwhelming them. TaskFlow is a professional product designed for real users, not a hackathon demo.

**Core Product Values**:
1. **Simplicity**: Clean, intuitive interface
2. **Reliability**: 99.9% uptime, data integrity, graceful error handling
3. **Performance**: Fast load times (<2s), instant interactions, optimistic UI
4. **Accessibility**: WCAG 2.1 AA compliance
5. **Privacy**: User data security, transparent data handling

**Target Users**:
- Individual Professionals
- Small Teams
- Students & Learners

### Core Principles to Consider in Specs

**I. Test-Driven Development (TDD)**
- Test coverage MUST be ≥85%
- Include testing strategy in specs (unit, integration, E2E)

**II. Type Safety First**
- Frontend: TypeScript strict mode, no `any` types
- Backend: Full Python type hints, mypy --strict
- API contracts MUST use TypeScript interfaces

**III. Graceful Degradation**
- Error boundaries for all routes
- Loading states for all async operations
- Friendly error messages, no stack traces in production

**IV. Full Documentation**
- OpenAPI/Swagger for all API endpoints
- Component documentation (Storybook)
- ADRs for architectural decisions
- **Context7 MCP**: MUST verify library documentation before implementation

**V. Evolutionary Architecture**
- Layer separation: Frontend (Components → Hooks → API Client) / Backend (Routes → Services → Repository)
- No cross-layer leakage

**VI. Simplicity & YAGNI**
- Smallest viable implementation
- No premature optimization

### UI/UX Standards (WCAG 2.1 AA)

- Semantic HTML with proper heading hierarchy
- All interactive elements keyboard accessible
- Focus indicators MUST be visible
- Color contrast ≥4.5:1 for text, ≥3:1 for large text
- ARIA labels for icon-only buttons
- Screen reader tested
- Touch targets ≥44px × 44px

### Responsive Design Breakpoints

- `sm: 640px` - Mobile landscape
- `md: 768px` - Tablet
- `lg: 1024px` - Desktop
- `xl: 1280px` - Large desktop

### Security Standards

**Authentication (Better Auth + JWT)**:
- All endpoints MUST require valid JWT token
- Users can only access/modify their own data
- Shared secret in environment variable `BETTER_AUTH_SECRET`

**Input Validation**:
- ALL inputs validated with Pydantic schemas
- HTML sanitized (XSS prevention)
- Parameterized queries (SQL injection prevention)
- Max payload: 1MB

**HTTPS & Headers**:
- HTTPS only in production
- `Secure` flag on cookies
- HSTS headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`

### Performance Standards

**Frontend**:
- First Contentful Paint (FCP) < 1.5s
- Largest Contentful Paint (LCP) < 2.5s
- Time to Interactive (TTI) < 3.5s
- Cumulative Layout Shift (CLS) < 0.1
- **Lighthouse Score ≥90**

**Backend**:
- Simple CRUD: < 200ms (p95)
- List endpoints: < 300ms (p95)
- Search queries: < 500ms (p95)

**Database**:
- Indexes on `user_id`, `created_at`, `completed`
- Avoid N+1 queries
- Paginate lists (max 100 items)

### Database Schema Conventions

**Naming**:
- Tables: Plural, snake_case (`tasks`, `users`)
- Columns: snake_case (`created_at`, `user_id`)
- Primary Keys: `id` (auto-incrementing integer)
- Foreign Keys: `{table}_id` (`user_id`, `task_id`)
- Timestamps: `created_at`, `updated_at` (UTC, automatic)

**SQLModel Pattern**:
```python
class ModelName(SQLModel, table=True):
    __tablename__ = "table_name"
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### API Design Standards

**RESTful Conventions**:
- GET `/api/tasks` - List all user tasks (200)
- POST `/api/tasks` - Create task (201, 400, 401)
- GET `/api/tasks/{id}` - Get task (200, 404)
- PATCH `/api/tasks/{id}` - Update task (200, 400, 404)
- DELETE `/api/tasks/{id}` - Delete task (204, 404)

**Response Format**:
```json
// Success
{ "id": 1, "title": "...", "completed": false }

// Error
{ "detail": "Task not found", "error_code": "TASK_NOT_FOUND" }
```

### Forbidden Practices

**Frontend**:
- ❌ No `any` type
- ❌ No `console.log` in production
- ❌ No inline styles
- ❌ No hardcoded URLs
- ❌ No unhandled promise rejections
- ❌ No missing loading/error states
- ❌ No accessibility violations
- ❌ No unoptimized images

**Backend**:
- ❌ No SQL string concatenation
- ❌ No plaintext passwords
- ❌ No missing type hints
- ❌ No unvalidated inputs
- ❌ No database models exposed to frontend

**General**:
- ❌ No library integration without Context7 verification
- ❌ No outdated API patterns (verify via Context7)
