<!--
  ============================================================================
  SYNC IMPACT REPORT
  ============================================================================
  Version Change: 2.0.0 → 2.1.0 (Context7 MCP integration requirement added)

  Modified Principles:
    - Full Documentation (Principle IV): Added Library Documentation (Context7 MCP) subsection
      requiring Context7 usage for all third-party library integrations

  Added Sections:
    - Library Documentation (Context7 MCP) under Full Documentation principle
    - Two new General Forbidden Practices for Context7 verification

  Removed Sections:
    - None

  Templates Status:
    - .specify/templates/plan-template.md ⚠ Requires Phase 2 architecture patterns
    - .specify/templates/spec-template.md ⚠ Requires UI/UX and API sections
    - .specify/templates/tasks-template.md ⚠ Requires frontend/backend task categories

  Follow-up TODOs:
    - Create phase-2-fullstack branch from phase-1-console
    - Update all templates to include Phase 2 sections and patterns
    - Create Tier 1 Phase 2 skills (spec-generator, plan-generator, auth-integrator, api-builder)
    - Integrate Context7 into all Phase 2 skills
    - Set up monorepo structure (frontend/, backend/, shared/)
    - Configure CI/CD pipelines for 8 quality gates
    - Establish design system with shadcn/ui
    - Configure Better Auth with JWT using Context7 docs
    - Set up Neon Serverless PostgreSQL database
    - Create OpenAPI documentation generation

  Previous Version History:
    - v1.0.0 (2025-12-27): Initial ratification for Phase 1
    - v1.1.0 (2025-12-27): Added branching strategy
    - v2.0.0 (2025-12-27): Phase 2 upgrade (Console → Full-Stack Web App)
  ============================================================================
-->

# TaskFlow Constitution

## Product Vision & Mission

**Product Name**: TaskFlow
**Tagline**: Intelligent Task Management That Adapts to You

**Mission**: Build a reliable, fast, and user-friendly task management platform that helps individuals and teams stay organized without overwhelming them. TaskFlow is a professional product designed for real users, not a hackathon demo.

**Target Users**:
- **Individual Professionals**: Knowledge workers needing simple, effective task tracking
- **Small Teams**: Collaborators wanting shared task visibility without enterprise complexity
- **Students & Learners**: Organized individuals managing multiple projects and deadlines

**Core Product Values**:
1. **Simplicity**: Clean, intuitive interface that gets out of your way
2. **Reliability**: 99.9% uptime, data integrity, graceful error handling
3. **Performance**: Fast load times (<2s), instant interactions, optimistic UI
4. **Accessibility**: WCAG 2.1 AA compliance, keyboard navigation, screen reader support
5. **Privacy**: User data security, transparent data handling, no third-party tracking

## Core Principles

### I. Test-Driven Development (TDD) - NON-NEGOTIABLE

Test-Driven Development is mandatory for all feature development across frontend and backend. This principle ensures code correctness, enables safe refactoring, and serves as living documentation.

- Tests MUST be written BEFORE implementation code
- Red-Green-Refactor cycle MUST be strictly enforced:
  1. **Red**: Write a failing test that defines expected behavior
  2. **Green**: Write minimal code to make the test pass
  3. **Refactor**: Improve code quality while keeping tests green
- **Frontend Testing**: React Testing Library for components, Vitest for logic
- **Backend Testing**: pytest for API routes, services, database operations
- **E2E Testing**: Playwright for critical user flows (signup, CRUD, notifications)
- Test coverage MUST be ≥85% for all production code
- No code merges are permitted without passing tests

**Rationale**: TDD catches bugs early, forces clear API design, and provides confidence for future changes. In a full-stack application, testing prevents regressions across multiple layers.

### II. Type Safety First

Static typing prevents entire categories of runtime errors and improves code maintainability. Strict typing applies to both TypeScript (frontend) and Python (backend).

**Frontend (TypeScript)**:
- Strict mode MUST be enabled in `tsconfig.json`
- No `any` types allowed except in rare, documented cases
- All props, hooks, and utilities MUST have explicit types
- Shared API contract types MUST live in `shared/types/`

**Backend (Python)**:
- Full type hints MUST be present on all functions, methods, and class attributes
- Strict mypy configuration MUST be enforced (no `Any` types)
- Pydantic models MUST be used for API request/response validation
- SQLModel MUST be used for database models (combines SQLAlchemy + Pydantic)

**Rationale**: Type safety enables IDE support, catches errors at development time, and serves as executable documentation. In a full-stack app, types enforce API contracts between frontend and backend.

### III. Graceful Degradation

The system MUST handle errors gracefully at every layer, providing meaningful feedback to users while maintaining stability.

**Frontend**:
- Error boundaries MUST wrap all route components
- Loading states MUST be shown for all async operations (skeletons/spinners)
- Optimistic UI updates with automatic rollback on failure
- Network errors display retry mechanisms, never crashes

**Backend**:
- API errors MUST return structured JSON with error codes and user-friendly messages
- Database errors MUST be caught and logged with full context
- Rate limiting prevents abuse without blocking legitimate users
- Health check endpoints enable monitoring (`/health`, `/api/health`)

**User Experience**:
- No stack traces visible in production UI
- User-facing messages MUST be friendly and actionable
- Empty states guide users toward first actions
- Fallbacks provided where possible (offline mode, cached data)

**Rationale**: Professional software handles edge cases gracefully. Users should never see a crash or cryptic error. Graceful degradation maintains trust and reduces support burden.

### IV. Full Documentation

Documentation is a first-class deliverable across all layers. Code without documentation is incomplete.

**Code-Level Documentation**:
- Docstrings MUST be present on all public functions, classes, and React components
- Each module/component folder MUST have README explaining purpose and usage
- Complex algorithms MUST include inline comments explaining "why" not "what"

**API Documentation**:
- OpenAPI/Swagger docs MUST be auto-generated from FastAPI routes
- All endpoints documented with request/response schemas, examples, error codes
- Authentication requirements clearly specified for each endpoint

**Component Documentation**:
- Storybook SHOULD be used for UI component library documentation
- Component props, variants, and usage examples documented

**Architecture Documentation**:
- Architecture Decision Records (ADRs) MUST capture significant decisions
- `specs/` folder organized by type (features/, api/, database/, ui/)
- System diagrams for data flow, authentication flow, deployment architecture

**Library Documentation (Context7 MCP)**:
- MUST use Context7 MCP server to fetch up-to-date documentation for all third-party libraries
- Before implementing integrations with Better Auth, Next.js, FastAPI, SQLModel, shadcn/ui, or any external library
- Verify current API patterns and best practices from source documentation
- Never rely solely on LLM knowledge for library-specific implementation details
- Document library versions used and reference Context7 docs in implementation comments and ADRs
- Use `mcp__context7__resolve-library-id` to find library IDs, then `mcp__context7__get-library-docs` for documentation

**Rationale**: Documentation enables team scaling, reduces onboarding time, and prevents knowledge silos. In a full-stack system, clear API and component docs are critical for collaboration. Context7 ensures we use current, accurate library documentation instead of outdated patterns.

### V. Evolutionary Architecture

Design for today's requirements while enabling tomorrow's growth. Use abstractions strategically across the full stack.

**Monorepo Structure**:
- Clean separation: `frontend/`, `backend/`, `shared/`
- Shared types and utilities centralized to prevent duplication
- Each workspace has independent dependency management

**Layer Separation**:
- **Frontend**: Components → Hooks → API Client → Services
- **Backend**: Routes → Services → Repository/ORM → Database
- No cross-layer leakage (e.g., database models never exposed to frontend)

**Strategic Abstractions**:
- Interfaces/Protocols MUST be used for components that will change
- Storage abstraction enables database swaps (Neon → local Postgres)
- Authentication abstraction enables provider swaps (Better Auth → Auth0)
- Minimal dependencies; prefer battle-tested libraries over novelty

**Rationale**: Over-engineering is as harmful as under-engineering. The right abstraction emerges from concrete use cases. Monorepo structure supports independent scaling while sharing common code.

### VI. Simplicity & YAGNI

Start with the smallest viable implementation. Add complexity only when requirements demand it.

- Implement the simplest solution that satisfies current requirements
- No premature optimization (profile first, optimize second)
- Three similar lines of code are better than one premature abstraction
- Delete dead code immediately; do not comment it out
- Use component libraries (shadcn/ui) to reduce custom CSS and maintain consistency

**Rationale**: Complexity is the enemy of reliability. Every line of code is a liability. Simple systems are easier to understand, test, and maintain. In full-stack apps, unnecessary complexity multiplies across layers.

## Phase 2 Technical Stack

This section defines the technology stack for Phase 2 (Full-Stack Web Application).

### Frontend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Next.js | 16+ | React framework with App Router |
| Language | TypeScript | 5.x+ | Type-safe JavaScript |
| Styling | Tailwind CSS | 3.x+ | Utility-first CSS framework |
| UI Components | shadcn/ui | Latest | Accessible, customizable components |
| Authentication | Better Auth | Latest | JWT-based authentication |
| State Management | React Context + Hooks | - | Global state (user, notifications) |
| HTTP Client | Fetch API | - | API communication |
| Forms | React Hook Form | Latest | Form validation & handling |
| Notifications | react-hot-toast | Latest | Toast notifications |
| Testing | Vitest + React Testing Library | Latest | Unit & component tests |
| E2E Testing | Playwright | Latest | Critical flow testing |

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | FastAPI | 0.115+ | Modern Python web framework |
| Language | Python | 3.13+ | Type-safe backend |
| ORM | SQLModel | Latest | Type-safe database models |
| Database | Neon Serverless PostgreSQL | - | Production database |
| Authentication | JWT (python-jose) | Latest | Stateless authentication |
| Validation | Pydantic | 2.x+ | Request/response validation |
| Migrations | Alembic | Latest | Database schema migrations |
| ASGI Server | Uvicorn | Latest | Production server |
| Testing | pytest | Latest | API & service tests |

### Infrastructure & Services

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend Deployment | Vercel | Next.js optimized hosting |
| Backend Deployment | Render / Railway | FastAPI hosting |
| Database Hosting | Neon | Serverless PostgreSQL |
| Email Service | Resend / SendGrid | Transactional emails |
| Monitoring | Sentry | Error tracking & monitoring |

### Development Tools

| Tool | Purpose |
|------|---------|
| Package Manager (Frontend) | pnpm | Fast, disk-efficient |
| Package Manager (Backend) | UV (Astral) | Fast Python package manager |
| Type Checking (Frontend) | TypeScript compiler | Static type checking |
| Type Checking (Backend) | mypy --strict | Static type checking |
| Linting (Frontend) | ESLint + Prettier | Code quality & formatting |
| Linting (Backend) | Ruff | Fast Python linter |

## Monorepo Structure Standards

TaskFlow uses a monorepo structure for frontend, backend, and shared code.

### Directory Structure

```
taskflow/
├── .spec-kit/                    # Spec-Kit Plus configuration
├── specs/                        # Organized specifications
│   ├── overview.md
│   ├── architecture.md
│   ├── features/                 # Feature specifications
│   ├── api/                      # API design docs
│   ├── database/                 # Database schema docs
│   └── ui/                       # UI/UX design docs
├── frontend/                     # Next.js application
│   ├── src/
│   │   ├── app/                 # App router pages
│   │   │   ├── (auth)/          # Protected routes
│   │   │   ├── (public)/        # Public routes
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/              # shadcn/ui components
│   │   │   ├── features/        # Feature components
│   │   │   └── layouts/         # Layout components
│   │   ├── lib/                 # Utilities & API client
│   │   ├── hooks/               # Custom React hooks
│   │   ├── types/               # Frontend-specific types
│   │   └── styles/              # Global styles
│   ├── public/                   # Static assets
│   ├── tests/                    # Frontend tests
│   ├── CLAUDE.md
│   ├── package.json
│   └── tsconfig.json
├── backend/                      # FastAPI application
│   ├── app/
│   │   ├── main.py              # Application entry
│   │   ├── models/              # SQLModel database models
│   │   ├── routes/              # API route handlers
│   │   ├── services/            # Business logic
│   │   ├── schemas/             # Pydantic request/response
│   │   ├── utils/               # Utilities
│   │   ├── middleware/          # Custom middleware
│   │   └── config.py            # Configuration
│   ├── tests/                   # Backend tests
│   ├── alembic/                 # Database migrations
│   ├── CLAUDE.md
│   ├── requirements.txt
│   └── pyproject.toml
├── shared/                       # Shared types & constants
│   ├── types/                    # TypeScript API types
│   └── schemas/                  # Pydantic schemas
├── CLAUDE.md                     # Root guidelines
├── docker-compose.yml
├── .github/workflows/            # CI/CD pipelines
└── README.md
```

### Structure Requirements

1. **Workspace Independence**: Each workspace (frontend/, backend/) MUST be independently runnable
2. **Shared Types**: API contract types MUST be defined once in `shared/` and imported by both
3. **No Cross-Imports**: Frontend MUST NOT import from backend; communication via API only
4. **Consistent Naming**: kebab-case for folders, PascalCase for React components, snake_case for Python

## Frontend Architecture Standards

### Component Organization

```
components/
├── ui/                          # shadcn/ui base components
│   ├── button.tsx
│   ├── input.tsx
│   ├── card.tsx
│   └── ...
├── features/                    # Feature-specific components
│   ├── task-list/
│   │   ├── task-list.tsx
│   │   ├── task-item.tsx
│   │   └── index.ts
│   └── auth/
│       ├── login-form.tsx
│       └── signup-form.tsx
└── layouts/                     # Page layouts
    ├── dashboard-layout.tsx
    └── auth-layout.tsx
```

### State Management

1. **Server State**: React Query / SWR for API data caching
2. **Global UI State**: React Context for theme, user session, notifications
3. **Local State**: useState / useReducer for component-specific state
4. **Form State**: React Hook Form for complex forms
5. **URL State**: Next.js router for filters, pagination

### Routing Conventions

- Use Next.js 16 App Router (not Pages Router)
- Route groups: `(auth)`, `(public)` for organization
- Dynamic routes: `[id]/page.tsx` for parameters
- Loading states: `loading.tsx` for automatic loading UI
- Error boundaries: `error.tsx` for route-level error handling

## Backend Architecture Standards

### Layer Separation

```
Request → Route Handler → Service → Repository → Database
```

**Route Layer** (`routes/`):
- Handle HTTP concerns (parsing, validation, response formatting)
- Validate input with Pydantic schemas
- Delegate business logic to services
- Return appropriate HTTP status codes

**Service Layer** (`services/`):
- Implement business logic
- Coordinate between multiple repositories
- Handle errors and return domain-specific exceptions
- No direct HTTP or database concerns

**Repository/ORM Layer**:
- Encapsulate database queries using SQLModel
- Return domain models
- Handle transaction management

### API Route Example

```python
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import TaskService
from app.auth import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    """Create a new task for the authenticated user."""
    try:
        task = await service.create_task(user_id=current_user.id, data=task_data)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## API Design Standards

### RESTful Conventions

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/api/tasks` | List all user tasks | 200 |
| POST | `/api/tasks` | Create task | 201, 400, 401 |
| GET | `/api/tasks/{id}` | Get task by ID | 200, 404 |
| PATCH | `/api/tasks/{id}` | Update task | 200, 400, 404 |
| DELETE | `/api/tasks/{id}` | Delete task | 204, 404 |
| PATCH | `/api/tasks/{id}/complete` | Toggle completion | 200, 404 |

### Authentication & Authorization

**Better Auth + JWT Integration**:
1. User logs in via Better Auth → Issues JWT access token
2. Frontend includes JWT in `Authorization: Bearer <token>` header
3. Backend verifies JWT signature using shared secret
4. Backend extracts user ID from token and enforces ownership
5. All API endpoints return only data belonging to authenticated user

**Security Requirements**:
- All endpoints MUST require valid JWT token
- Requests without token receive `401 Unauthorized`
- Users can only access/modify their own tasks
- Shared secret stored in environment variable `BETTER_AUTH_SECRET`

### Request/Response Format

**Success Response**:
```json
{
  "id": 1,
  "title": "Complete Phase 2",
  "description": "Build full-stack web app",
  "completed": false,
  "created_at": "2025-12-27T10:00:00Z"
}
```

**Error Response**:
```json
{
  "detail": "Task not found",
  "error_code": "TASK_NOT_FOUND"
}
```

## Database Schema Standards

### Naming Conventions

- **Tables**: Plural, snake_case (`tasks`, `users`)
- **Columns**: snake_case (`created_at`, `user_id`)
- **Primary Keys**: `id` (auto-incrementing integer)
- **Foreign Keys**: `{table}_id` (`user_id`, `task_id`)
- **Timestamps**: `created_at`, `updated_at` (UTC, automatic)

### SQLModel Pattern

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Task database model."""
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = None
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Migration Standards

- Use Alembic for all schema changes
- Every migration MUST have `upgrade()` and `downgrade()` functions
- Migrations MUST be transactional
- Test migrations on staging before production
- Include comments explaining complex migrations

## UI/UX Standards

### Design System (shadcn/ui)

- Use shadcn/ui as foundation for all UI components
- Customize theme via `tailwind.config.js`
- Extend components in `components/ui/` only when necessary
- Never modify shadcn/ui source; compose instead

### Responsive Design

**Breakpoints** (Tailwind):
- `sm: 640px` - Mobile landscape
- `md: 768px` - Tablet
- `lg: 1024px` - Desktop
- `xl: 1280px` - Large desktop

**Mobile-First**:
- Design for mobile first, enhance for larger screens
- Touch targets MUST be ≥44px × 44px
- Text readable at 16px base size without zoom
- Navigation optimized for mobile (hamburger menu)

### Accessibility (WCAG 2.1 AA)

**Requirements**:
- Semantic HTML with proper heading hierarchy
- All interactive elements keyboard accessible
- Focus indicators MUST be visible
- Color contrast ≥4.5:1 for text, ≥3:1 for large text
- ARIA labels for icon-only buttons
- Screen reader tested (NVDA or VoiceOver)

### Loading & Error States

**Loading States**:
- Skeleton loaders for content
- Spinners for actions
- Progress indicators for multi-step processes

**Empty States**:
- Friendly messaging when no data exists
- Helpful CTAs guiding users to action
- Illustrative icons/graphics

**Error States**:
- User-friendly error messages (no technical jargon)
- Recovery actions (retry, go back, contact support)
- Never show stack traces in production

## Security Standards

### Authentication (Better Auth + JWT)

**JWT Implementation**:
- Access tokens: Short-lived (15 minutes), stored in httpOnly cookie
- Refresh tokens: Long-lived (7 days), stored in httpOnly cookie
- Token claims: user ID, email, issued at, expires at
- Signature: HS256 with secret from environment variable

**Password Security**:
- Hash passwords with bcrypt (cost factor ≥12)
- Minimum length: 8 characters
- No password logging or display

### Data Protection

**Input Validation**:
- Validate ALL inputs with Pydantic schemas
- Sanitize HTML to prevent XSS
- Use parameterized queries (SQLModel prevents SQL injection)
- Reject excessively large payloads (max 1MB)

**HTTPS & Headers**:
- HTTPS only in production
- Set `Secure` flag on cookies
- Use HSTS headers (`Strict-Transport-Security`)
- Set `X-Content-Type-Options: nosniff`
- Set `X-Frame-Options: DENY`

**CORS Configuration**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://taskflow.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

### Environment Variables

**Required Secrets**:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret (min 32 chars, random)
- `EMAIL_API_KEY`: Email service API key (Resend/SendGrid)
- `FRONTEND_URL`: Frontend origin for CORS

**Storage**:
- Use `.env` files for local dev (gitignored)
- Use platform environment variables for production
- Never commit secrets to git

## Performance Standards

### Page Load Time Targets

| Metric | Target | Tool |
|--------|--------|------|
| First Contentful Paint (FCP) | < 1.5s | Lighthouse |
| Largest Contentful Paint (LCP) | < 2.5s | Lighthouse |
| Time to Interactive (TTI) | < 3.5s | Lighthouse |
| Cumulative Layout Shift (CLS) | < 0.1 | Lighthouse |
| **Lighthouse Score** | **≥90** | Lighthouse |

### API Response Time Targets

| Endpoint Type | Target (p95) |
|--------------|--------------|
| Simple CRUD | < 200ms |
| List endpoints | < 300ms |
| Search queries | < 500ms |

### Optimization Strategies

**Frontend**:
- Code splitting and lazy loading
- Image optimization (Next.js `<Image>`, WebP)
- Font optimization (preload, `font-display: swap`)
- Bundle size < 200KB (gzipped)
- Stale-while-revalidate caching

**Backend**:
- Database indexes on `user_id`, `created_at`, `completed`
- Avoid N+1 queries (use joins, eager loading)
- Paginate list endpoints (max 100 items)
- Connection pooling for database
- Compression (gzip/brotli)

## Notification Standards

### Email Notifications

**Service**: Resend or SendGrid

**Email Types**:
1. **Welcome Email**: Sent on signup
   - Subject: "Welcome to TaskFlow 🎉"
   - Content: Product intro, getting started guide
2. **Task Reminders**: Sent for tasks with due dates
   - Subject: "Task Due Soon: {task_title}"
   - Content: Task details, link to dashboard

**Standards**:
- HTML templates with plain text fallback
- Unsubscribe link in footer
- Mobile-responsive design
- Personalized with user's name

### Browser Notifications

**Permission Flow**:
- Ask after user signs up (not immediately)
- Explain value ("Get reminders for your tasks")
- Respect user's choice (don't re-ask if denied)

**Standards**:
- Use Web Push API
- Show only when tab not focused
- Include action buttons ("View Task", "Dismiss")
- Respect quiet hours (8 PM - 8 AM local time)

### In-App Notifications (Toast)

**Toast Types**:
- **Success**: Green ("Task created")
- **Error**: Red ("Failed to delete task")
- **Warning**: Yellow ("Unsaved changes")
- **Info**: Blue ("Task shared with you")

**Standards**:
- Duration: 4 seconds (user can dismiss earlier)
- Max 3 toasts visible at once
- Position: Top-right corner
- Include undo for destructive operations

## Professional Features Requirements

TaskFlow MUST include these professional features beyond basic CRUD:

1. **Onboarding Flow**: 3-step welcome wizard for new users
2. **Empty States**: Friendly messaging + helpful CTAs when no tasks
3. **Search**: Fast, fuzzy search across titles/descriptions (Cmd+K shortcut)
4. **Keyboard Shortcuts**: N (new task), S (search), Escape (close), ? (help)
5. **Dark Mode**: Theme toggle with system preference detection
6. **Export/Import**: Tasks as JSON or CSV with metadata preservation
7. **Activity Log**: Audit trail of user actions (create, update, delete, complete)
8. **Settings Page**: Profile, notification preferences, theme, account deletion
9. **Help Center**: FAQ, searchable articles, contact support
10. **Feedback Widget**: Simple form for bug reports and feature requests

## Forbidden Practices

The following practices are STRICTLY PROHIBITED and MUST block code merges:

### Frontend Forbidden

- ❌ No `any` type in TypeScript (use `unknown` if type truly unknown)
- ❌ No `console.log` in production code (use proper logging)
- ❌ No inline styles (use Tailwind classes)
- ❌ No hardcoded URLs (use environment variables)
- ❌ No unhandled promise rejections (always catch errors)
- ❌ No missing loading states (show skeleton/spinner)
- ❌ No missing error boundaries (wrap routes)
- ❌ No accessibility violations (test with Lighthouse)
- ❌ No unoptimized images (use Next.js `<Image>`)
- ❌ No exposed API keys (use environment variables)

### Backend Forbidden

- ❌ No SQL string concatenation (use SQLModel parameterized queries)
- ❌ No plaintext passwords (always hash with bcrypt)
- ❌ No missing type hints (all functions must have return annotations)
- ❌ No unvalidated inputs (use Pydantic schemas)
- ❌ No database models exposed to frontend (use Pydantic response schemas)
- ❌ No synchronous blocking in async routes (use `await` for I/O)
- ❌ No missing error handling (catch exceptions, return structured errors)
- ❌ No hardcoded credentials (use environment variables)

### General Forbidden

- ❌ No commented-out code (delete unused code)
- ❌ No `TODO` comments without issue reference (create ticket, link in comment)
- ❌ No large files in git (use .gitignore)
- ❌ No force pushes to protected branches (main, phase branches)
- ❌ No skipping tests (tests must pass before merge)
- ❌ No bypassing linting (fix errors, don't disable rules)
- ❌ No library integration without Context7 documentation verification (always fetch current docs first)
- ❌ No outdated API patterns (verify current library APIs via Context7 before implementation)

## Enhanced Quality Gates

All code MUST pass these 8 gates before merge:

### 1. Specification Gate
- Feature MUST have approved specification in `specs/features/`
- User flows documented with diagrams
- API contracts defined (request/response schemas)
- UI mockups or wireframes provided

### 2. Design Gate
- UI/UX designs approved
- Component inventory complete
- Accessibility considerations documented
- Mobile and desktop designs provided

### 3. Architecture Gate
- System design reviewed (data flow, layer separation)
- Technology stack confirmed (no unapproved dependencies)
- Performance implications considered
- Security review completed

### 4. Implementation Gate
- Code review passed (minimum 1 reviewer)
- All tests passing (unit, integration, E2E)
- No linting errors (ESLint, Ruff)
- Type checking passed (TypeScript, mypy --strict)

### 5. Security Gate
- No known vulnerabilities (npm audit, safety check)
- Secrets not committed to git
- Input validation implemented
- OWASP Top 10 considerations reviewed

### 6. Performance Gate
- Lighthouse score ≥90 (Performance, Accessibility, Best Practices, SEO)
- Page load time < 2s (measured on staging)
- API response times meet targets (p95 < 300ms for CRUD)
- No performance regressions

### 7. Accessibility Gate
- WCAG 2.1 AA compliance verified
- Keyboard navigation tested
- Screen reader tested (NVDA or VoiceOver)
- Color contrast verified (≥4.5:1 for text)

### 8. Deployment Gate
- Successful deployment to staging
- Health check endpoints passing (`/health`, `/api/health`)
- Database migrations applied successfully
- Smoke tests passed (critical flows work)

## Branching Strategy

TaskFlow uses a phase-based branching strategy to support incremental evolution.

### Branch Structure

| Branch | Purpose | Base |
|--------|---------|------|
| `master` | Production-ready code, constitution, shared artifacts | - |
| `phase-1-console` | Phase 1: Python console application (COMPLETE) | master |
| `phase-2-fullstack` | **Phase 2: Next.js + FastAPI + PostgreSQL (CURRENT)** | phase-1-console |
| `phase-3-ai-chatbot` | Phase 3: AI chatbot with MCP + OpenAI Agents | phase-2-fullstack |
| `phase-4-kubernetes` | Phase 4: Local Kubernetes with Minikube | phase-3-ai-chatbot |
| `phase-5-cloud` | Phase 5: Cloud deployment with Kafka + Dapr | phase-4-kubernetes |

### Branch Rules

- **Current Phase**: `phase-2-fullstack` (Full-Stack Web Application)
- Each phase branch MUST be created from its predecessor
- Phase branches MUST NOT be deleted after creation
- Work on a phase MUST happen on that phase's branch
- Feature branches follow pattern: `phase-2/<feature-name>`
- PRs within a phase target that phase's branch

### Workflow

```
master (constitution, shared docs)
  └── phase-1-console (COMPLETE)
  └── phase-2-fullstack (CURRENT)
        ├── phase-2/frontend-setup
        ├── phase-2/backend-api
        ├── phase-2/authentication
        ├── phase-2/task-crud-ui
        └── phase-2/notifications
```

## Development Workflow

### Local Development Setup

**Prerequisites**:
- Node.js 18+, pnpm
- Python 3.13+, UV
- Docker (for local PostgreSQL)

**Setup**:
1. Clone repo and checkout `phase-2-fullstack` branch
2. Install dependencies: `cd frontend && pnpm install` + `cd backend && uv sync`
3. Start database: `docker-compose up -d postgres`
4. Run migrations: `cd backend && alembic upgrade head`
5. Start backend: `cd backend && uvicorn app.main:app --reload`
6. Start frontend: `cd frontend && pnpm dev`
7. Open `http://localhost:3000`

### Commit Standards

- Commits MUST be atomic (one logical change)
- Follow Conventional Commits: `<type>(<scope>): <description>`
- Types: `feat`, `fix`, `test`, `docs`, `refactor`, `style`, `chore`, `perf`
- Scopes: `frontend`, `backend`, `api`, `ui`, `db`, etc.
- Examples:
  - `feat(frontend): add task creation modal`
  - `fix(api): handle missing user ID in task creation`
  - `test(backend): add unit tests for task service`

### Pull Request Process

1. Create feature branch: `git checkout -b phase-2/feature-name`
2. Implement using TDD (Red-Green-Refactor)
3. Run quality gates locally:
   - Frontend: `pnpm lint && pnpm type-check && pnpm test`
   - Backend: `uv run pytest && uv run mypy . && uv run ruff check`
4. Commit with conventional commit messages
5. Push and create PR targeting `phase-2-fullstack`
6. Wait for CI to pass (automated quality gates)
7. Request review
8. Merge after all 8 gates pass (squash merge)

## Governance

This constitution is the supreme authority for TaskFlow development. All code, designs, and decisions MUST comply with these principles.

### Amendment Process

1. Propose amendment with rationale
2. Document impact on existing code
3. Obtain approval from project owner
4. Update constitution with new version
5. Update Sync Impact Report
6. Migrate non-compliant code (if any)
7. Update dependent templates

### Versioning Policy

Constitution follows semantic versioning:
- **MAJOR**: Principle removal, backward-incompatible redefinition, or scope change (Phase 1 → Phase 2)
- **MINOR**: New principle added or existing principle materially expanded
- **PATCH**: Clarifications, typos, non-semantic refinements

### Compliance Review

- All PRs MUST verify compliance with constitution
- Non-compliance MUST be documented with justification
- Unjustified violations MUST block merge
- Periodic audits SHOULD verify ongoing compliance (quarterly)

### Amendment History

- **v1.0.0** (2025-12-27): Initial ratification for Phase 1 (Console Application)
- **v1.1.0** (2025-12-27): Added branching strategy for multi-phase development
- **v2.0.0** (2025-12-27): **Phase 2 upgrade** (Console → Full-Stack Web App)
  - Added Product Vision & Mission
  - Expanded Core Principles for full-stack context
  - Replaced Phase 1 Constraints with Phase 2 Technical Stack
  - Added 8 new architecture/standards sections (Monorepo, Frontend, Backend, API, Database, UI/UX, Security, Performance)
  - Added Notification Standards and Professional Features
  - Added Forbidden Practices section
  - Enhanced Quality Gates (5 → 8 gates)
  - Updated Branching Strategy (current: phase-2-fullstack)
- **v2.1.0** (2025-12-27): **Context7 MCP integration requirement**
  - Added Library Documentation (Context7 MCP) to Full Documentation principle
  - Mandated Context7 usage for all third-party library integrations
  - Added forbidden practices for library integration without Context7 verification
  - Updated to ensure current, accurate library documentation usage

---

**Version**: 2.1.0
**Ratified**: 2025-12-27 (Phase 1)
**Last Amended**: 2025-12-27 (Context7 MCP integration)
**Current Phase**: Phase 2 - Full-Stack Web Application
