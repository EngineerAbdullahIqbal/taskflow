# TaskFlow - Phase 2 Full-Stack Web Application

**Status**: Phase 1 (Setup) Complete ✅ | Phase 2 (Foundational) In Progress 🚧

TaskFlow is a full-stack task and habit tracking web application with rich features including priorities, categories, scheduling, and multi-channel reminders.

## Architecture

This is a **monorepo** with independent workspaces:

```
Task-Flow/
├── frontend/          # Next.js 16 App Router + TypeScript + shadcn/ui
├── backend/           # FastAPI + SQLModel + Python 3.13
├── shared/            # TypeScript types shared between frontend/backend
└── .github/workflows/ # CI/CD pipelines
```

## Tech Stack

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5.x (strict mode)
- **UI**: shadcn/ui + Tailwind CSS v4
- **Auth**: Better Auth (JWT)
- **Forms**: React Hook Form + Zod validation
- **State**: React hooks + Server Components
- **Notifications**: react-hot-toast + Web Push API

### Backend
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.13 (mypy --strict)
- **ORM**: SQLModel with AsyncSession
- **Validation**: Pydantic 2.x
- **Auth**: JWT (python-jose) + bcrypt
- **Migrations**: Alembic
- **Server**: Uvicorn (ASGI)
- **Background Jobs**: Celery/APScheduler
- **Email**: Resend/SendGrid

### Database
- **Primary**: Neon Serverless PostgreSQL
- **Cache/Queue**: Redis (for background jobs)

## Quick Start

### Prerequisites
- **Node.js**: 18+ (for frontend)
- **Python**: 3.13+ (for backend)
- **pnpm**: Latest (frontend package manager)
- **uv**: Latest (backend package manager)
- **PostgreSQL**: Neon account or local instance

### Frontend Setup

```bash
cd frontend
pnpm install
cp .env.example .env.local
# Edit .env.local with your configuration
pnpm dev
```

Frontend runs on http://localhost:3000

### Backend Setup

```bash
cd backend
uv sync
cp .env.example .env
# Edit .env with your DATABASE_URL and secrets
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Backend API runs on http://localhost:8000

## Features

### Phase 2 User Stories (MVP)

1. **[P1] User Registration & Login** - JWT authentication with Better Auth
2. **[P1] Rich Task Creation** - Story, priority (Low/Medium/High/Urgent), categories, scheduling
3. **[P2] Task Reminders** - Email + browser notifications with notification center
4. **[P2] Complete & Delete Tasks** - Task lifecycle management
5. **[P2] Edit Tasks** - Update all task fields
6. **[P3] Filter & Sort** - Advanced task list functionality
7. **[P3] Responsive Design** - Mobile/tablet/desktop layouts

### Database Schema

- `users` - User accounts with email/password
- `tasks` - Rich tasks with story, priority, schedule, categories, reminders
- `categories` - User-created categories with colors (max 20 per user)
- `notifications` - Notification history (30-day retention)
- `notification_preferences` - User reminder settings (email/browser)

## Development Commands

### Frontend

```bash
pnpm dev          # Start dev server
pnpm build        # Production build
pnpm lint         # ESLint + Prettier
pnpm type-check   # TypeScript validation
```

### Backend

```bash
uv run uvicorn app.main:app --reload  # Start dev server
uv run pytest                          # Run tests
uv run ruff check .                    # Lint code
uv run mypy .                          # Type checking
uv run alembic revision --autogenerate # Create migration
uv run alembic upgrade head            # Apply migrations
```

## API Endpoints

- `POST /auth/signup` - Create account
- `POST /auth/login` - Login with JWT
- `POST /auth/logout` - Logout
- `GET /api/tasks` - List user tasks (with filters/sorts)
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task details
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `POST /api/tasks/{id}/complete` - Mark complete
- `GET /api/categories` - List categories
- `POST /api/categories` - Create category
- `GET /api/notifications` - List notifications
- `PATCH /api/notifications/{id}` - Mark read/clicked
- `GET /api/preferences` - Get notification preferences
- `PATCH /api/preferences` - Update preferences

## Project Structure

### Frontend
```
frontend/src/
├── app/              # Next.js 16 App Router pages
├── components/
│   ├── ui/          # shadcn/ui components
│   └── features/    # Feature-specific components
├── lib/
│   ├── api/         # API client with JWT
│   ├── auth-config.ts  # Better Auth config
│   └── auth-context.tsx # Auth React context
└── types/           # TypeScript types
```

### Backend
```
backend/app/
├── main.py          # FastAPI app entry
├── config.py        # Environment config
├── models/          # SQLModel database models
├── schemas/         # Pydantic request/response schemas
├── services/        # Business logic layer
├── routes/          # API route handlers
├── middleware/      # Auth + error handling middleware
├── utils/           # Shared utilities
└── jobs/            # Background job schedulers
```

## Configuration

### Environment Variables

See `.env.example` files in `frontend/` and `backend/` for required configuration.

**Critical Secrets**:
- `BETTER_AUTH_SECRET` - Min 32 chars for JWT signing
- `JWT_SECRET_KEY` - Backend JWT verification
- `DATABASE_URL` - PostgreSQL connection string
- `RESEND_API_KEY` or `SENDGRID_API_KEY` - Email notifications

## Testing

### Frontend
```bash
pnpm test        # Vitest unit tests
pnpm test:e2e    # Playwright E2E tests
```

### Backend
```bash
uv run pytest                    # All tests
uv run pytest --cov=app          # With coverage
uv run pytest tests/unit         # Unit tests only
uv run pytest tests/integration  # Integration tests only
```

**Target Coverage**: ≥85%

## Deployment

### Frontend (Vercel)
1. Connect GitHub repo to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy from `001-ps2-fullstack-web-foundation` branch

### Backend (Render/Railway)
1. Create new Web Service
2. Set build command: `uv sync`
3. Set start command: `uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables
5. Deploy

### Database (Neon)
1. Create Neon PostgreSQL database
2. Copy connection string to `DATABASE_URL`
3. Run migrations: `uv run alembic upgrade head`

## Performance Goals

- Page load: < 2s (FCP < 1.5s, LCP < 2.5s)
- API response: < 300ms (p95) for CRUD operations
- Lighthouse score: ≥90 (all categories)
- Support: 100 concurrent users

## Security

- **Authentication**: JWT with 15-min access tokens, 7-day refresh tokens
- **Password Hashing**: bcrypt (cost factor 12)
- **Input Validation**: Pydantic schemas on all API requests
- **Rate Limiting**: 5 auth attempts per 15 minutes
- **CORS**: Configured for frontend origin only
- **SQL Injection**: Prevented via SQLModel ORM parameterization

## Contributing

1. Create feature branch from `001-ps2-fullstack-web-foundation`
2. Follow atomic task breakdown in `specs/001-ps2-fullstack-web-foundation/tasks.md`
3. Run linters and type checkers before commit
4. Ensure tests pass
5. Create PR with description

## License

MIT

## Support

For issues or questions, create a GitHub issue.
