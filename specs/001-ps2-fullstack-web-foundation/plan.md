# Implementation Plan: Phase 2 Full-Stack Web Application Foundation

**Branch**: `001-ps2-fullstack-web-foundation` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ps2-fullstack-web-foundation/spec.md`

**Note**: This plan follows the Spec-Driven Development (SDD) workflow and TaskFlow Constitution v2.1.0.

## Summary

Transform TaskFlow from a Phase 1 console application into a production-ready full-stack web application with multi-user authentication, rich task/habit tracking (story, priority, schedule, categories), task reminders (email + browser notifications), notification center, and responsive UI. The application will support user registration, secure JWT-based login, comprehensive task CRUD operations with filtering/sorting, proactive reminder notifications, and deployment on Vercel (frontend) + Render/Railway (backend) + Neon PostgreSQL (database).

**Primary Technical Approach**:
- **Frontend**: Next.js 16+ App Router with TypeScript, shadcn/ui, Tailwind CSS, Better Auth for authentication, Web Push API for browser notifications, notification center with bell icon
- **Backend**: FastAPI with SQLModel ORM, JWT verification, Pydantic validation, Alembic migrations, background job scheduler for reminders (Celery/APScheduler), email service integration (Resend/SendGrid)
- **Database**: Neon Serverless PostgreSQL with 5 tables (users, tasks, categories, notifications, notification_preferences) and indexed columns for user_id, priority, category_id, due_date, reminder_time
- **Deployment**: Vercel (frontend), Render/Railway (backend with background worker), Neon (database)

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x+, Node.js 18+
- Backend: Python 3.13+

**Primary Dependencies**:
- Frontend: Next.js 16+, Better Auth, shadcn/ui, Tailwind CSS, React Hook Form, react-hot-toast, Web Push API
- Backend: FastAPI 0.115+, SQLModel, Pydantic 2.x+, python-jose (JWT), bcrypt, Alembic, Uvicorn, Celery or APScheduler (background jobs), Resend or SendGrid (email), Redis (job queue)

**Storage**:
- Neon Serverless PostgreSQL with five tables:
  - `users` (id, email, name, password_hash, created_at, updated_at)
  - `tasks` (id, user_id, title, story, priority, schedule, due_date, category_id, reminder_enabled, reminder_timing, reminder_channels, completed, created_at, updated_at)
  - `categories` (id, user_id, name, color, created_at, updated_at)
  - `notifications` (id, user_id, task_id, type, title, message, read, clicked, created_at)
  - `notification_preferences` (id, user_id, reminder_email, email_notifications_enabled, browser_notifications_enabled, created_at, updated_at)

**Testing**:
- Frontend: Vitest + React Testing Library (component tests), Playwright (E2E tests)
- Backend: pytest (unit + integration tests), pytest-asyncio (async tests)
- Target coverage: ≥85%

**Target Platform**:
- Frontend: Modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
- Backend: Linux server (Uvicorn ASGI)
- Database: Neon Serverless PostgreSQL (cloud-hosted)

**Project Type**: Web application (monorepo with frontend/ and backend/ workspaces)

**Performance Goals**:
- Page load time < 2s (FCP < 1.5s, LCP < 2.5s)
- API response time < 300ms (p95) for CRUD operations
- Lighthouse score ≥90 (Performance, Accessibility, Best Practices, SEO)
- Support 100 concurrent users without degradation

**Constraints**:
- WCAG 2.1 AA accessibility compliance
- Mobile-first responsive design (< 640px, 640px-1024px, > 1024px)
- JWT access tokens expire in 15 minutes, refresh tokens in 7 days
- Maximum 20 categories per user
- Task title max 200 characters, story max 2000 characters

**Scale/Scope**:
- 7 user stories (Authentication, Create/View Rich Tasks, Complete/Delete, Edit, Filter/Sort, Responsive, Reminders)
- 88 functional requirements across 9 categories
- 6 API resource endpoints (auth, tasks, categories, notifications, user preferences, health)
- 5 database tables with foreign key relationships
- 13 success criteria with measurable outcomes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Specification Gate ✅
- [x] Feature has approved specification in `specs/001-ps2-fullstack-web-foundation/spec.md`
- [x] User flows documented with acceptance scenarios (52 total scenarios across 7 user stories)
- [x] API contracts defined (14 endpoints with request/response schemas)
- [x] UI requirements specified (task creation form, category management, filters/sorts, responsive, notification center, reminder settings)

### Gate 2: Design Gate ⏳ (Pending Phase 1)
- [ ] UI/UX designs approved (wireframes for task list, creation form, category selector, notification center, reminder settings)
- [ ] Component inventory complete (TaskList, TaskItem, CreateTaskModal, CategoryBadge, PriorityIndicator, FilterPanel, NotificationBell, NotificationCenter, ReminderSettings)
- [ ] Accessibility considerations documented (keyboard navigation, screen reader labels, color contrast, notification announcements)
- [ ] Mobile and desktop designs provided (responsive breakpoints: 640px, 768px, 1024px)

### Gate 3: Architecture Gate ⏳ (Pending Phase 1)
- [ ] System design reviewed (layered architecture: Routes → Services → ORM → Database, background job scheduler for reminders)
- [ ] Technology stack confirmed (Next.js 16+, FastAPI, SQLModel, Better Auth, Neon PostgreSQL, Celery/APScheduler, Resend/SendGrid, Redis)
- [ ] Performance implications considered (database indexes, pagination, code splitting, notification job queue management)
- [ ] Security review completed (JWT verification, bcrypt password hashing, input validation, CORS, email verification, notification permissions)

### Gate 4: Implementation Gate ⏳ (Pending Implementation)
- [ ] Code review passed (minimum 1 reviewer)
- [ ] All tests passing (unit, integration, E2E)
- [ ] No linting errors (ESLint + Prettier for frontend, Ruff for backend)
- [ ] Type checking passed (TypeScript strict mode, mypy --strict)

### Gate 5: Security Gate ⏳ (Pending Implementation)
- [ ] No known vulnerabilities (npm audit, safety check)
- [ ] Secrets not committed to git (BETTER_AUTH_SECRET, DATABASE_URL)
- [ ] Input validation implemented (Pydantic schemas for all API requests)
- [ ] OWASP Top 10 considerations reviewed (SQL injection prevention, XSS sanitization, rate limiting)

### Gate 6: Performance Gate ⏳ (Pending Deployment)
- [ ] Lighthouse score ≥90 (Performance, Accessibility, Best Practices, SEO)
- [ ] Page load time < 2s (measured on staging)
- [ ] API response times meet targets (p95 < 300ms for CRUD)
- [ ] No performance regressions

### Gate 7: Accessibility Gate ⏳ (Pending Implementation)
- [ ] WCAG 2.1 AA compliance verified (Lighthouse accessibility audit)
- [ ] Keyboard navigation tested (Tab, Enter, Escape, Cmd+K for search)
- [ ] Screen reader tested (NVDA or VoiceOver)
- [ ] Color contrast verified (≥4.5:1 for text, priority indicators: Low=#3B82F6, Medium=#EAB308, High=#F97316, Urgent=#EF4444)

### Gate 8: Deployment Gate ⏳ (Pending Deployment)
- [ ] Successful deployment to staging (Vercel preview for frontend, Render/Railway for backend)
- [ ] Health check endpoints passing (`/health` frontend, `/api/health` backend)
- [ ] Database migrations applied successfully (Alembic upgrade head)
- [ ] Smoke tests passed (signup → login → create task → mark complete → delete)

**Constitution Violations**: None. All requirements align with TaskFlow Constitution v2.1.0.

## Project Structure

### Documentation (this feature)

```text
specs/001-ps2-fullstack-web-foundation/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (/sp.plan output)
├── research.md          # Phase 0 output (library patterns, best practices)
├── data-model.md        # Phase 1 output (entity models, relationships)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API OpenAPI schemas)
│   ├── auth.yaml        # Authentication endpoints
│   ├── tasks.yaml       # Task CRUD endpoints
│   ├── categories.yaml  # Category CRUD endpoints
│   ├── notifications.yaml # Notification endpoints
│   └── preferences.yaml # User notification preferences endpoints
├── checklists/
│   └── requirements.md  # Specification validation (COMPLETE)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application (monorepo structure per Constitution)
frontend/
├── src/
│   ├── app/                      # Next.js 16 App Router
│   │   ├── (auth)/               # Protected routes
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx      # Task dashboard (list, filters, sorts)
│   │   │   │   └── layout.tsx    # Dashboard layout with nav
│   │   │   ├── tasks/
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx  # Task detail/edit page
│   │   │   └── settings/
│   │   │       └── page.tsx      # User settings (categories, preferences)
│   │   ├── (public)/             # Public routes
│   │   │   ├── login/
│   │   │   │   └── page.tsx      # Login form
│   │   │   └── signup/
│   │   │       └── page.tsx      # Signup form
│   │   ├── layout.tsx            # Root layout (auth provider, theme)
│   │   └── page.tsx              # Landing page (redirect to dashboard or login)
│   ├── components/
│   │   ├── ui/                   # shadcn/ui base components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   ├── select.tsx
│   │   │   ├── badge.tsx
│   │   │   └── ...
│   │   ├── features/             # Feature-specific components
│   │   │   ├── tasks/
│   │   │   │   ├── TaskList.tsx          # Main task list
│   │   │   │   ├── TaskItem.tsx          # Individual task card
│   │   │   │   ├── CreateTaskModal.tsx   # Task creation form
│   │   │   │   ├── EditTaskModal.tsx     # Task edit form
│   │   │   │   ├── PriorityIndicator.tsx # Priority badge (Low/Med/High/Urgent)
│   │   │   │   └── FilterPanel.tsx       # Status/priority/category filters
│   │   │   ├── categories/
│   │   │   │   ├── CategoryBadge.tsx     # Category display with color
│   │   │   │   ├── CategorySelector.tsx  # Dropdown with on-the-fly creation
│   │   │   │   └── CategoryManager.tsx   # Category CRUD interface
│   │   │   ├── notifications/
│   │   │   │   ├── NotificationBell.tsx  # Bell icon with unread count in top bar
│   │   │   │   ├── NotificationCenter.tsx # Dropdown notification list
│   │   │   │   ├── NotificationItem.tsx  # Individual notification card
│   │   │   │   └── ReminderSettings.tsx  # Reminder config in task form
│   │   │   └── auth/
│   │   │       ├── LoginForm.tsx         # Email/password login
│   │   │       ├── SignupForm.tsx        # Email/password/name signup
│   │   │       └── ProtectedRoute.tsx    # Auth guard wrapper
│   │   └── layouts/              # Page layouts
│   │       ├── DashboardLayout.tsx
│   │       └── AuthLayout.tsx
│   ├── lib/                      # Utilities & API client
│   │   ├── api/
│   │   │   ├── client.ts         # Base fetch wrapper with JWT header
│   │   │   ├── tasks.ts          # Task API calls
│   │   │   ├── categories.ts     # Category API calls
│   │   │   ├── notifications.ts  # Notification API calls
│   │   │   ├── preferences.ts    # User preferences API calls
│   │   │   └── auth.ts           # Auth API calls
│   │   ├── auth-context.tsx      # Better Auth React context
│   │   ├── notification-service.ts # Web Push API & notification permissions
│   │   └── utils.ts              # Helper functions
│   ├── hooks/                    # Custom React hooks
│   │   ├── useTasks.ts           # Task fetching/mutation
│   │   ├── useCategories.ts      # Category fetching/mutation
│   │   ├── useNotifications.ts   # Notification fetching/marking read
│   │   └── useAuth.ts            # Auth state management
│   ├── types/                    # Frontend-specific types
│   │   ├── task.ts               # Task interface
│   │   ├── category.ts           # Category interface
│   │   ├── notification.ts       # Notification interface
│   │   └── user.ts               # User interface
│   └── styles/
│       └── globals.css           # Tailwind imports, custom styles
├── public/                       # Static assets
│   ├── favicon.ico
│   └── logo.svg
├── tests/                        # Frontend tests
│   ├── components/
│   │   ├── TaskItem.test.tsx
│   │   └── CreateTaskModal.test.tsx
│   └── e2e/
│       ├── auth.spec.ts          # Login/signup flows
│       └── tasks.spec.ts         # Task CRUD flows
├── .env.example
├── CLAUDE.md
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── playwright.config.ts

backend/
├── app/
│   ├── main.py                   # FastAPI application entry
│   ├── config.py                 # Configuration (env vars)
│   ├── models/                   # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py               # User model (id, email, name, password_hash)
│   │   ├── task.py               # Task model (title, story, priority, schedule, due_date, category_id, reminder fields, completed)
│   │   ├── category.py           # Category model (name, color)
│   │   ├── notification.py       # Notification model (user_id, task_id, type, title, message, read, clicked)
│   │   └── notification_preference.py # NotificationPreference model (user_id, reminder_email, email/browser enabled)
│   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── auth.py               # LoginRequest, SignupRequest, TokenResponse
│   │   ├── task.py               # TaskCreate, TaskUpdate, TaskResponse
│   │   ├── category.py           # CategoryCreate, CategoryUpdate, CategoryResponse
│   │   ├── notification.py       # NotificationResponse, MarkReadRequest
│   │   └── preference.py         # NotificationPreferenceUpdate, NotificationPreferenceResponse
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py       # Password hashing, JWT generation
│   │   ├── task_service.py       # Task CRUD with ownership verification
│   │   ├── category_service.py   # Category CRUD with 20-category limit
│   │   ├── notification_service.py # Notification CRUD, mark read/clicked
│   │   └── email_service.py      # Email sending via Resend/SendGrid
│   ├── routes/                   # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py               # POST /auth/signup, /auth/login, /auth/logout
│   │   ├── tasks.py              # GET/POST /api/tasks, GET/PATCH/DELETE /api/tasks/{id}
│   │   ├── categories.py         # GET/POST /api/categories, PUT/DELETE /api/categories/{id}
│   │   ├── notifications.py      # GET /api/notifications, PATCH /api/notifications/{id}/read
│   │   ├── preferences.py        # GET/PUT /api/user/notification-preferences
│   │   └── health.py             # GET /api/health
│   ├── jobs/                     # Background job tasks
│   │   ├── __init__.py
│   │   ├── reminder_scheduler.py # Main scheduler loop checking pending reminders
│   │   └── reminder_processor.py # Send browser/email notifications for due reminders
│   ├── middleware/               # Custom middleware
│   │   ├── __init__.py
│   │   ├── auth.py               # JWT verification dependency
│   │   └── error_handler.py      # Global error handling
│   ├── utils/                    # Utilities
│   │   ├── __init__.py
│   │   ├── database.py           # Database session management
│   │   └── jwt.py                # JWT encoding/decoding
│   ├── templates/                # Email templates
│   │   ├── __init__.py
│   │   ├── reminder_email.html   # HTML email template for task reminders
│   │   └── reminder_email.txt    # Plain text fallback for reminders
│   └── migrations/               # Database migration scripts (Alembic alternative)
│       └── 20251228_initial_schema.py
├── alembic/                      # Alembic migrations
│   ├── versions/
│   │   ├── 001_create_users_table.py
│   │   ├── 002_create_categories_table.py
│   │   ├── 003_create_tasks_table.py
│   │   ├── 004_create_notifications_table.py
│   │   └── 005_create_notification_preferences_table.py
│   ├── env.py
│   └── script.py.mako
├── tests/                        # Backend tests
│   ├── conftest.py               # Pytest fixtures
│   ├── routes/
│   │   ├── test_auth.py          # Auth endpoint tests
│   │   ├── test_tasks.py         # Task endpoint tests
│   │   ├── test_categories.py    # Category endpoint tests
│   │   ├── test_notifications.py # Notification endpoint tests
│   │   └── test_preferences.py   # User preferences endpoint tests
│   ├── services/
│   │   ├── test_auth_service.py
│   │   ├── test_task_service.py
│   │   ├── test_category_service.py
│   │   ├── test_notification_service.py
│   │   └── test_email_service.py
│   ├── jobs/
│   │   ├── test_reminder_scheduler.py
│   │   └── test_reminder_processor.py
│   └── models/
│       ├── test_user.py
│       ├── test_task.py
│       ├── test_category.py
│       ├── test_notification.py
│       └── test_notification_preference.py
├── .env.example
├── CLAUDE.md
├── requirements.txt
├── pyproject.toml               # UV/pip configuration
└── alembic.ini

shared/                           # Shared types (if needed)
├── types/
│   └── api.ts                    # Shared API contract types

.github/workflows/
├── frontend-ci.yml               # Frontend quality gates
└── backend-ci.yml                # Backend quality gates

docker-compose.yml                # Local PostgreSQL for development
.env.example                      # Root environment template
CLAUDE.md                         # Root guidelines
README.md                         # Project setup instructions
```

**Structure Decision**: Web application monorepo with clean separation between frontend (Next.js), backend (FastAPI), and shared types. This aligns with TaskFlow Constitution Section "Monorepo Structure Standards" and supports independent workspace management while enabling code sharing.

## Complexity Tracking

**Constitution Violations**: None

All requirements align with TaskFlow Constitution v2.1.0:
- ✅ TDD enforced (≥85% test coverage requirement)
- ✅ Type safety (TypeScript strict mode, Python mypy --strict)
- ✅ Graceful degradation (error boundaries, loading states, structured API errors)
- ✅ Full documentation (OpenAPI for APIs, component docs, ADRs for significant decisions)
- ✅ Library documentation via Context7 MCP (required for Better Auth, Next.js, FastAPI, SQLModel, shadcn/ui)
- ✅ Evolutionary architecture (layered separation, no cross-layer leakage)
- ✅ Simplicity & YAGNI (smallest viable implementation, no premature optimization)
- ✅ All 8 quality gates addressed
- ✅ Monorepo structure with frontend/, backend/, shared/
- ✅ Security standards (JWT, bcrypt, input validation, CORS)
- ✅ Performance standards (Lighthouse ≥90, API < 300ms, page load < 2s)

---

## Phase 0: Research & Best Practices

**Objective**: Resolve all unknowns in Technical Context by researching library patterns via Context7 MCP and documenting decisions.

### Research Tasks

1. **Better Auth + JWT Integration Pattern**
   - Use Context7 to fetch Better Auth documentation: `/better-auth/better-auth`
   - Research: JWT plugin configuration, shared secret setup between Next.js and FastAPI
   - Decision: Document recommended approach for stateless JWT authentication
   - Output: `research.md` section "Better Auth JWT Strategy"

2. **Next.js 16 App Router Best Practices**
   - Use Context7 to fetch Next.js documentation: `/vercel/next.js`
   - Research: Route groups, loading states, error boundaries, middleware for auth
   - Decision: Document recommended folder structure for (auth) and (public) routes
   - Output: `research.md` section "Next.js App Router Patterns"

3. **FastAPI + SQLModel Integration**
   - Use Context7 to fetch FastAPI documentation: `/fastapi/fastapi`
   - Use Context7 to fetch SQLModel documentation: `/tiangolo/sqlmodel`
   - Research: Dependency injection, async database sessions, Pydantic integration
   - Decision: Document recommended service layer pattern and session management
   - Output: `research.md` section "FastAPI + SQLModel Architecture"

4. **shadcn/ui Component Setup**
   - Use Context7 to fetch shadcn/ui documentation: `/shadcn/ui`
   - Research: Installation with Next.js App Router, Tailwind configuration, component customization
   - Decision: Document which base components needed (Button, Input, Card, Select, Badge, Modal)
   - Output: `research.md` section "shadcn/ui Component Inventory"

5. **Neon PostgreSQL Connection Pooling**
   - Research: Neon Serverless PostgreSQL best practices for connection pooling
   - Decision: Document recommended connection string format and pool size
   - Output: `research.md` section "Neon Database Configuration"

6. **Priority and Category UI Patterns**
   - Research: Best practices for priority indicators (color coding: Low=blue, Medium=yellow, High=orange, Urgent=red)
   - Research: Category badge UI patterns with on-the-fly creation
   - Decision: Document recommended component designs and accessibility considerations
   - Output: `research.md` section "Rich Task UI Patterns"

7. **Alembic Migration Workflow**
   - Research: Alembic best practices for SQLModel, migration testing, rollback strategies
   - Decision: Document migration file structure and naming conventions
   - Output: `research.md` section "Database Migration Strategy"

8. **Email Service Integration (Resend/SendGrid)**
   - Use Context7 to fetch Resend or SendGrid documentation
   - Research: Email template design best practices, transactional email delivery, rate limiting, failure handling
   - Decision: Document email service selection (Resend vs SendGrid), template structure (HTML + plain text), delivery reliability approach
   - Output: `research.md` section "Email Service Configuration"

9. **Background Job Scheduler (Celery/APScheduler)**
   - Use Context7 to fetch Celery or APScheduler documentation
   - Research: Job scheduling patterns, task queue management, failure handling, deployment with FastAPI
   - Decision: Document scheduler choice (Celery with Redis vs APScheduler in-memory), reminder processing workflow, failure retry strategy
   - Output: `research.md` section "Reminder Job Scheduler"

**Output**: `research.md` with 9 sections documenting all decisions, rationales, and Context7-verified patterns.

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete with all Context7 verifications

### 1. Data Model Design

**Objective**: Extract entities from feature spec and define SQLModel models with relationships.

**Entity: User**
```python
# File: backend/app/models/user.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """User account model managed by Better Auth."""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    password_hash: str = Field(max_length=255)  # bcrypt hash
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Entity: Category**
```python
# File: backend/app/models/category.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Category(SQLModel, table=True):
    """User-created task category with name and color."""
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=50)  # Unique per user (enforced at service layer)
    color: str = Field(max_length=7)  # Hex code e.g., "#3B82F6"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Unique constraint: (user_id, name) at database level
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )
```

**Entity: Task**
```python
# File: backend/app/models/task.py
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime, date
from typing import Optional, List
from enum import Enum

class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ReminderTiming(str, Enum):
    FIVE_MIN_BEFORE = "5min_before"
    FIFTEEN_MIN_BEFORE = "15min_before"
    ONE_HOUR_BEFORE = "1hour_before"
    ONE_DAY_BEFORE = "1day_before"
    AT_TIME = "at_time"

class Task(SQLModel, table=True):
    """Task or recurring habit with rich metadata and reminder settings."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    story: Optional[str] = Field(default=None, max_length=2000)  # Markdown supported
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM, index=True)
    schedule: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))  # ["Monday", "Wednesday"]
    due_date: Optional[date] = Field(default=None, index=True)  # Mutually exclusive with schedule
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id", index=True)
    reminder_enabled: bool = Field(default=False)
    reminder_timing: Optional[ReminderTiming] = Field(default=None)
    reminder_channels: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))  # ["browser", "email"]
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Entity: Notification**
```python
# File: backend/app/models/notification.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class NotificationType(str, Enum):
    REMINDER = "reminder"
    SYSTEM = "system"

class Notification(SQLModel, table=True):
    """In-app notification for notification center."""
    __tablename__ = "notifications"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")  # Nullable if task deleted
    type: NotificationType = Field(default=NotificationType.REMINDER)
    title: str = Field(max_length=200)
    message: str = Field(max_length=500)
    read: bool = Field(default=False, index=True)
    clicked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

**Entity: NotificationPreference**
```python
# File: backend/app/models/notification_preference.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class NotificationPreference(SQLModel, table=True):
    """User notification preferences for email and browser notifications."""
    __tablename__ = "notification_preferences"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, index=True)
    reminder_email: str = Field(max_length=255)  # Defaults to user's account email
    email_notifications_enabled: bool = Field(default=True)
    browser_notifications_enabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Relationships**:
- User (1) → Tasks (N): One user owns many tasks
- User (1) → Categories (N): One user owns many categories
- User (1) → Notifications (N): One user receives many notifications
- User (1) → NotificationPreference (1): One user has one notification preference record
- Category (1) → Tasks (N): One category assigned to many tasks (nullable)
- Task (1) → Notifications (N): One task may generate multiple notifications (nullable, cascade on delete)

**Indexes**:
- `users.email` (unique, for login lookups)
- `tasks.user_id` (for filtering user tasks)
- `tasks.completed` (for status filtering)
- `tasks.priority` (for priority filtering)
- `tasks.category_id` (for category filtering)
- `tasks.due_date` (for date sorting and reminder scheduling)
- `tasks.created_at` (for creation date sorting)
- `categories.user_id` (for user category lookups)
- `notifications.user_id` (for fetching user notifications)
- `notifications.read` (for filtering unread notifications)
- `notifications.created_at` (for sorting notifications by recency)
- `notification_preferences.user_id` (unique, for fetching user preferences)

**Validation Rules**:
- Task title: 1-200 characters (required)
- Task story: 0-2000 characters (optional)
- Priority: enum (low, medium, high, urgent)
- Schedule: JSON array of day names OR null (mutually exclusive with due_date)
- Due date: ISO date format OR null (mutually exclusive with schedule)
- Reminder timing: enum (5min_before, 15min_before, 1hour_before, 1day_before, at_time) OR null
- Reminder channels: JSON array containing "browser" and/or "email" OR null
- Category name: 1-50 characters, unique per user (case-insensitive)
- Category color: 7-character hex code (e.g., "#3B82F6")
- Max 20 categories per user (enforced at service layer)
- Notification title: 1-200 characters (required)
- Notification message: 1-500 characters (required)
- Reminder email: valid email format (defaults to user's account email)

**Output**: `data-model.md` with complete entity definitions, relationships, indexes, and validation rules.

### 2. API Contract Design

**Objective**: Generate OpenAPI schemas for all API endpoints from functional requirements.

**Authentication Endpoints** (`contracts/auth.yaml`):
```yaml
openapi: 3.1.0
info:
  title: TaskFlow Authentication API
  version: 1.0.0

paths:
  /auth/signup:
    post:
      summary: Create new user account
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password, name]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
                name:
                  type: string
                  maxLength: 255
      responses:
        '201':
          description: Account created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenResponse'
        '400':
          description: Invalid input or email already exists
        '429':
          description: Rate limit exceeded

  /auth/login:
    post:
      summary: Authenticate user and issue JWT tokens
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        '200':
          description: Authentication successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenResponse'
        '401':
          description: Invalid credentials
        '429':
          description: Rate limit exceeded (5 attempts per 15 minutes)

components:
  schemas:
    TokenResponse:
      type: object
      properties:
        access_token:
          type: string
        refresh_token:
          type: string
        token_type:
          type: string
          enum: [bearer]
        expires_in:
          type: integer
          description: Seconds until access token expires (900 for 15 minutes)
```

**Task Endpoints** (`contracts/tasks.yaml`):
```yaml
openapi: 3.1.0
info:
  title: TaskFlow Tasks API
  version: 1.0.0

paths:
  /api/tasks:
    get:
      summary: List user tasks with filtering and sorting
      security:
        - bearerAuth: []
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [all, pending, completed]
        - name: priority
          in: query
          schema:
            type: string
            enum: [all, low, medium, high, urgent]
        - name: category_id
          in: query
          schema:
            type: integer
        - name: sort
          in: query
          schema:
            type: string
            enum: [created_desc, created_asc, due_date_asc, priority_desc, title_asc]
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items:
                      $ref: '#/components/schemas/TaskResponse'
                  total:
                    type: integer
                  page:
                    type: integer
                  limit:
                    type: integer
        '401':
          description: Unauthorized (invalid or missing JWT)

    post:
      summary: Create new task
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskResponse'
        '400':
          description: Invalid input
        '401':
          description: Unauthorized

  /api/tasks/{id}:
    get:
      summary: Get task by ID
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Task details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskResponse'
        '404':
          description: Task not found or not owned by user

    patch:
      summary: Update task
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
      responses:
        '200':
          description: Task updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskResponse'
        '400':
          description: Invalid input
        '404':
          description: Task not found

    delete:
      summary: Delete task
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '204':
          description: Task deleted successfully
        '404':
          description: Task not found

  /api/tasks/{id}/complete:
    patch:
      summary: Toggle task completion status
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Completion status toggled
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskResponse'
        '404':
          description: Task not found

components:
  schemas:
    TaskCreate:
      type: object
      required: [title]
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        story:
          type: string
          maxLength: 2000
        priority:
          type: string
          enum: [low, medium, high, urgent]
          default: medium
        schedule:
          type: array
          items:
            type: string
            enum: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
          description: For recurring habits (mutually exclusive with due_date)
        due_date:
          type: string
          format: date
          description: For one-time tasks (mutually exclusive with schedule)
        category_id:
          type: integer
          nullable: true
        reminder_enabled:
          type: boolean
          default: false
        reminder_timing:
          type: string
          enum: [5min_before, 15min_before, 1hour_before, 1day_before, at_time]
          nullable: true
        reminder_channels:
          type: array
          items:
            type: string
            enum: [browser, email]
          nullable: true
          description: Notification channels for reminders

    TaskUpdate:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        story:
          type: string
          maxLength: 2000
        priority:
          type: string
          enum: [low, medium, high, urgent]
        schedule:
          type: array
          items:
            type: string
        due_date:
          type: string
          format: date
        category_id:
          type: integer
          nullable: true
        reminder_enabled:
          type: boolean
        reminder_timing:
          type: string
          enum: [5min_before, 15min_before, 1hour_before, 1day_before, at_time]
          nullable: true
        reminder_channels:
          type: array
          items:
            type: string
            enum: [browser, email]
          nullable: true
        completed:
          type: boolean

    TaskResponse:
      type: object
      properties:
        id:
          type: integer
        user_id:
          type: integer
        title:
          type: string
        story:
          type: string
          nullable: true
        priority:
          type: string
          enum: [low, medium, high, urgent]
        schedule:
          type: array
          items:
            type: string
          nullable: true
        due_date:
          type: string
          format: date
          nullable: true
        category_id:
          type: integer
          nullable: true
        category:
          $ref: '#/components/schemas/CategoryResponse'
          nullable: true
        reminder_enabled:
          type: boolean
        reminder_timing:
          type: string
          enum: [5min_before, 15min_before, 1hour_before, 1day_before, at_time]
          nullable: true
        reminder_channels:
          type: array
          items:
            type: string
            enum: [browser, email]
          nullable: true
        completed:
          type: boolean
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    CategoryResponse:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        color:
          type: string

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

**Category Endpoints** (`contracts/categories.yaml`):
```yaml
openapi: 3.1.0
info:
  title: TaskFlow Categories API
  version: 1.0.0

paths:
  /api/categories:
    get:
      summary: List user categories
      security:
        - bearerAuth: []
      responses:
        '200':
          description: List of categories
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CategoryResponse'
        '401':
          description: Unauthorized

    post:
      summary: Create new category
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CategoryCreate'
      responses:
        '201':
          description: Category created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CategoryResponse'
        '400':
          description: Invalid input or duplicate name
        '409':
          description: Maximum 20 categories per user

  /api/categories/{id}:
    put:
      summary: Update category
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CategoryUpdate'
      responses:
        '200':
          description: Category updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CategoryResponse'
        '404':
          description: Category not found

    delete:
      summary: Delete category
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '204':
          description: Category deleted successfully (tasks retain data, category_id set to null)
        '404':
          description: Category not found

components:
  schemas:
    CategoryCreate:
      type: object
      required: [name, color]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 50
        color:
          type: string
          pattern: '^#[0-9A-Fa-f]{6}$'

    CategoryUpdate:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 50
        color:
          type: string
          pattern: '^#[0-9A-Fa-f]{6}$'

    CategoryResponse:
      type: object
      properties:
        id:
          type: integer
        user_id:
          type: integer
        name:
          type: string
        color:
          type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

**Notification Endpoints** (`contracts/notifications.yaml`):
```yaml
openapi: 3.1.0
info:
  title: TaskFlow Notifications API
  version: 1.0.0

paths:
  /api/notifications:
    get:
      summary: List user notifications for notification center
      security:
        - bearerAuth: []
      parameters:
        - name: unread_only
          in: query
          schema:
            type: boolean
            default: false
      responses:
        '200':
          description: List of notifications
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/NotificationResponse'

  /api/notifications/{id}/read:
    patch:
      summary: Mark notification as read
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Notification marked as read
        '404':
          description: Notification not found

components:
  schemas:
    NotificationResponse:
      type: object
      properties:
        id:
          type: integer
        user_id:
          type: integer
        task_id:
          type: integer
          nullable: true
        type:
          type: string
          enum: [reminder, system]
        title:
          type: string
        message:
          type: string
        read:
          type: boolean
        clicked:
          type: boolean
        created_at:
          type: string
          format: date-time

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

**User Notification Preferences Endpoints** (`contracts/preferences.yaml`):
```yaml
openapi: 3.1.0
info:
  title: TaskFlow User Notification Preferences API
  version: 1.0.0

paths:
  /api/user/notification-preferences:
    get:
      summary: Get user notification preferences
      security:
        - bearerAuth: []
      responses:
        '200':
          description: User notification preferences
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NotificationPreferenceResponse'

    put:
      summary: Update user notification preferences
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NotificationPreferenceUpdate'
      responses:
        '200':
          description: Preferences updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NotificationPreferenceResponse'
        '400':
          description: Invalid input

components:
  schemas:
    NotificationPreferenceUpdate:
      type: object
      properties:
        reminder_email:
          type: string
          format: email
        email_notifications_enabled:
          type: boolean
        browser_notifications_enabled:
          type: boolean

    NotificationPreferenceResponse:
      type: object
      properties:
        id:
          type: integer
        user_id:
          type: integer
        reminder_email:
          type: string
        email_notifications_enabled:
          type: boolean
        browser_notifications_enabled:
          type: boolean
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

**Output**: `contracts/` directory with `auth.yaml`, `tasks.yaml`, `categories.yaml`, `notifications.yaml`, `preferences.yaml` OpenAPI 3.1 schemas.

### 3. Quickstart Guide

**Objective**: Document local development setup and deployment instructions.

**Output**: `quickstart.md` with:
- Prerequisites (Node.js 18+, Python 3.13+, Docker, pnpm, UV)
- Local setup steps (clone, install deps, start database, run migrations, start servers)
- Environment variable configuration (DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL)
- Running tests (frontend: `pnpm test`, backend: `uv run pytest`)
- Running quality gates (linting, type checking, coverage)
- Deployment instructions (Vercel frontend, Render backend, Neon database)

### 4. Agent Context Update

**Objective**: Update Claude Code agent context with new Phase 2 technologies.

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Expected additions to CLAUDE.md**:
- Next.js 16 App Router patterns
- FastAPI + SQLModel integration
- Better Auth JWT configuration
- shadcn/ui component usage
- Alembic migration workflow
- Neon PostgreSQL connection pooling

---

## Architecture Decision Records (ADRs)

Based on the plan, the following ADRs should be created:

### ADR-001: JWT Authentication Strategy
**Decision**: Use Better Auth with stateless JWT tokens (access: 15min, refresh: 7 days) shared between Next.js frontend and FastAPI backend.

**Context**: Need secure, scalable authentication for multi-user web app.

**Alternatives Considered**:
1. Session-based auth with database storage
2. OAuth 2.0 with Auth0/Clerk
3. Better Auth with stateless JWT (CHOSEN)

**Rationale**:
- Stateless JWT reduces database load (no session table)
- Better Auth provides type-safe React hooks
- Shared secret enables backend JWT verification
- 15-minute access tokens balance security and UX
- 7-day refresh tokens reduce re-login friction

**Consequences**:
- ✅ Scalable (no session database)
- ✅ Fast (no database lookup per request)
- ⚠️ Token revocation requires workaround (blacklist or short expiration)
- ⚠️ Shared secret must be securely managed

### ADR-002: Monorepo Structure with Independent Workspaces
**Decision**: Use monorepo with frontend/, backend/, shared/ workspaces and independent package management (pnpm for frontend, UV for backend).

**Context**: Need to share types between frontend and backend while maintaining clean separation.

**Alternatives Considered**:
1. Separate repositories for frontend and backend
2. Monorepo with unified package manager (CHOSEN)
3. Polyrepo with published shared package

**Rationale**:
- Shared types reduce API contract duplication
- Atomic commits for cross-stack features
- Simplified CI/CD (single repo for deployments)
- Independent workspaces prevent dependency conflicts

**Consequences**:
- ✅ Type safety across stack
- ✅ Easier feature development (no cross-repo PRs)
- ⚠️ Requires discipline to avoid frontend → backend imports

### ADR-003: Priority and Category as First-Class Task Features
**Decision**: Include priority (Low/Medium/High/Urgent) and categories (user-created, max 20) as core task fields in Phase 2 MVP.

**Context**: User explicitly requested rich task tracking with priority, schedule, and categories.

**Alternatives Considered**:
1. Basic task CRUD only (defer priority/categories to Phase 3)
2. Priority only (defer categories)
3. Full rich task features (CHOSEN)

**Rationale**:
- User feedback indicated these features are essential for professional task management
- Adding later would require schema migration and UI refactoring
- Competitive task apps (Todoist, TickTick) include these as baseline features
- Adds minimal complexity (4 priority levels, 1 category table)

**Consequences**:
- ✅ Professional-grade task management from day one
- ✅ Differentiation from basic todo apps
- ⚠️ Increased initial implementation scope
- ⚠️ Additional UI components needed (priority badges, category selectors)

### ADR-004: Notification Delivery Strategy - Background Job Scheduler with Dual Channels
**Decision**: Use background job scheduler (Celery with Redis or APScheduler) to process task reminders and send notifications via both browser (Web Push API) and email (Resend/SendGrid).

**Context**: User requested reminder functionality with email and browser notifications, requiring reliable scheduled delivery at exact times.

**Alternatives Considered**:
1. Serverless cron jobs (Vercel Cron, GitHub Actions) for reminder processing
2. Background job scheduler with Redis queue (CHOSEN - Celery or APScheduler)
3. Client-side reminder scheduling with browser localStorage

**Rationale**:
- Background scheduler provides sub-minute precision for reminder delivery (check every 60 seconds)
- Redis queue ensures reliability with persistence and retry capability
- Dual-channel delivery (browser + email) maximizes user reach regardless of browser state
- Web Push API enables native browser notifications with "bell icon" notification center
- Email fallback ensures critical reminders are delivered even if browser closed
- Celery/APScheduler patterns well-documented via Context7 for FastAPI integration

**Implementation Details**:
- Reminder scheduler runs every 60 seconds checking `tasks` table for pending reminders
- Calculate reminder time from `due_date` or next `schedule` occurrence minus `reminder_timing` offset
- Create `Notification` record in database for notification center persistence
- Send browser notification via Web Push API (if permission granted and channel enabled)
- Send email via Resend/SendGrid (if channel enabled, using `notification_preferences.reminder_email`)
- Auto-cancel reminders when task marked complete or deleted (cascade delete)
- Notification center retains records for 30 days with manual dismiss option

**Consequences**:
- ✅ Reliable reminder delivery within 30 seconds of scheduled time
- ✅ Dual-channel approach maximizes notification reach
- ✅ Persistent notification center provides historical record
- ✅ Graceful fallback (email if browser closed, in-app if browser permission denied)
- ⚠️ Requires Redis deployment alongside PostgreSQL
- ⚠️ Email service cost (Resend free tier: 3,000 emails/month, then $0.10/1,000)
- ⚠️ Background worker process deployment alongside API server

---

## Next Steps

1. **Create ADRs**: Document the 4 architectural decisions above in `history/adr/`
2. **Execute Phase 0**: Use Context7 MCP to fetch library documentation and generate `research.md`
3. **Execute Phase 1**: Generate `data-model.md`, `contracts/`, `quickstart.md`
4. **Run agent context update**: `.specify/scripts/bash/update-agent-context.sh claude`
5. **Re-validate Constitution Check**: Ensure all Phase 1 design decisions pass gates
6. **Run `/sp.tasks`**: Generate actionable task breakdown from this plan

---

**Plan Created**: 2025-12-28
**Next Command**: `/sp.tasks` (after Phase 0 and Phase 1 artifacts generated)
**Constitution Compliance**: ✅ All gates aligned with TaskFlow Constitution v2.1.0
