# TaskFlow - Intelligent Task Management System

An evolution-first task management system developed across 5 phases, from console to cloud-native AI platform.

## Project Structure

```
TaskFlow/
├── .specify/                    # Specification framework (SpecifyPlus)
├── specs/                       # Feature specifications
│   └── phase-1-console/
│       ├── spec.md
│       ├── plan.md
│       ├── data-model.md
│       ├── research.md
│       ├── quickstart.md
│       └── tasks.md
├── history/                     # Architecture decision records & prompts
│   ├── adr/
│   │   ├── ADR-001-...
│   │   └── ADR-002-...
│   └── prompts/
├── .claude/                     # Claude Code skills
│   └── skills/
│       ├── quality-gate/
│       ├── tdd-enforcer/
│       └── python-scaffold/
│
└── phase-1-console/             # Phase 1: Console Application
    ├── src/                     # Source code
    ├── tests/                   # Test suite
    ├── .venv/                   # Virtual environment
    ├── pyproject.toml           # Project config
    ├── README-phase1.md
    └── .gitignore
```

## Phases

### Phase 1: Console Application ✅ COMPLETE
**Status**: Foundation Complete, All 6 User Stories Implemented

- Interactive menu-driven CLI
- In-memory storage
- TDD methodology
- Full type safety (mypy --strict)

**Setup**:
```bash
cd phase-1-console/
uv sync
uv run pytest
uv run mypy --strict src/
uv run python -m src.main
```

### Phase 2: Full-Stack Web Application (Current) 🚀
**Status**: Phase 4 Frontend Complete, Backend Integration Next

**Tech Stack**:
- **Frontend**: Next.js 16 App Router + TypeScript + shadcn/ui + Tailwind CSS + Better Auth
- **Backend**: FastAPI + SQLModel + PostgreSQL + JWT + Alembic
- **Database**: Neon Serverless PostgreSQL
- **Deployment**: Vercel (frontend) + Render/Railway (backend)

**Completed**:
- ✅ Phase 1: Setup (monorepo structure, dependencies, CI/CD)
- ✅ Phase 2: Foundation (database, authentication, API infrastructure)
- ✅ Phase 3: User Story 1 - Registration & Login (JWT auth)
- ✅ Phase 4 Frontend: Rich Task Creation & Viewing UI

**In Progress**:
- ⏳ Phase 4 Backend: Task/Category API endpoints (T051-T062)

**Setup (Development)**:

```bash
# Frontend (Next.js)
cd frontend/
pnpm install
pnpm dev
# Runs on http://localhost:3000

# Backend (FastAPI)
cd backend/
uv sync
uv run alembic upgrade head  # Run migrations
uv run uvicorn app.main:app --reload
# Runs on http://localhost:8000
# API docs: http://localhost:8000/docs
```

**Environment Variables**:
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here

# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow
JWT_SECRET_KEY=your-jwt-secret-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
```

### Phase 3: AI Features (Future)
- AI-powered task analysis
- Smart categorization
- Intelligent scheduling

### Phase 4: Kubernetes Deployment (Future)
- Container orchestration
- Scalable microservices
- Cloud-native deployment

### Phase 5: Collaborative Platform (Future)
- Multi-user support
- Real-time collaboration
- Team management

## Architecture

All phases follow these principles:

1. **Test-Driven Development (TDD)** - Tests written FIRST
2. **Type Safety** - mypy --strict enforced
3. **Graceful Degradation** - User-friendly error handling
4. **Full Documentation** - Architecture docs & ADRs
5. **Evolutionary Design** - Built for future expansion
6. **Simplicity (YAGNI)** - Minimal viable implementation

## Key Resources

- **Constitution**: [.specify/memory/constitution.md](.specify/memory/constitution.md) - Project principles
- **Phase 1 Spec**: [specs/phase-1-console/spec.md](specs/phase-1-console/spec.md)
- **Implementation Plan**: [specs/phase-1-console/plan.md](specs/phase-1-console/plan.md)
- **Task Breakdown**: [specs/phase-1-console/tasks.md](specs/phase-1-console/tasks.md)
- **Architecture Decisions**:
  - [ADR-001: Three-Layer Architecture](history/adr/ADR-001-three-layer-architecture-with-protocol-abstraction.md)
  - [ADR-002: Data Modeling](history/adr/ADR-002-data-modeling-with-dataclass-and-validation.md)

## Development Tools

- **Quality Gate**: `uv run python ./.claude/skills/quality-gate/scripts/run_gates.py src/`
- **TDD Enforcer**: `uv run python ./.claude/skills/tdd-enforcer/scripts/tdd_check.py src/`
- **Python Scaffold**: `uv run python ./.claude/skills/python-scaffold/scripts/scaffold.py module <name>`

## Getting Started

### Phase 1 (Console App)
```bash
cd phase-1-console/
uv sync
uv run pytest
uv run mypy --strict src/
uv run python -m src.main
```

### Phase 2 (Web App) - Current Development

**1. Start Backend (Terminal 1)**:
```bash
cd backend/

# First time setup
uv sync
cp .env.example .env  # Edit with your database credentials

# Run database migrations
uv run alembic upgrade head

# Start FastAPI server
uv run uvicorn app.main:app --reload

# Server runs on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

**2. Start Frontend (Terminal 2)**:
```bash
cd frontend/

# First time setup
pnpm install
cp .env.example .env.local  # Edit with backend URL

# Start Next.js dev server
pnpm dev

# App runs on http://localhost:3000
```

**3. Access the App**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

**4. Test the UI** (Phase 4 Frontend):
- Navigate to http://localhost:3000/dashboard
- Click "Create Task" button
- Fill in:
  - Title (required, 1-200 chars)
  - Story (optional, max 2000 chars, markdown supported)
  - Priority (Low/Medium/High/Urgent)
  - Schedule (recurring habit: Mon/Wed/Fri) OR Due Date (one-time task)
  - Category (select existing or create new with color)
- Submit to see glassmorphism card with animations

## Quick Reference

### Phase 1 (Console)
| Command | Purpose |
|---------|---------|
| `uv run pytest` | Run all tests |
| `uv run mypy --strict src/` | Type check |
| `uv run ruff check src/` | Lint code |
| `uv run python -m src.main` | Run console app |

### Phase 2 (Web App)
| Command | Purpose |
|---------|---------|
| **Backend** | |
| `uv run uvicorn app.main:app --reload` | Start FastAPI server |
| `uv run alembic upgrade head` | Run database migrations |
| `uv run pytest` | Run backend tests |
| `uv run mypy --strict app/` | Type check backend |
| **Frontend** | |
| `pnpm dev` | Start Next.js dev server |
| `pnpm build` | Build for production |
| `pnpm type-check` | Run TypeScript checks |
| `pnpm lint` | Run ESLint |

## Contributing

1. Follow TDD: Write tests FIRST
2. Ensure mypy --strict passes
3. Update documentation as you go
4. Create ADRs for architectural decisions
5. One task = one commit

## License

MIT License

---

**Last Updated**: 2025-12-28
**Current Phase**: 2 (Full-Stack Web Application)
**Status**: Phase 4 Frontend Complete (Rich Task UI with Glassmorphism), Backend Integration Next
