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

### Phase 1: Console Application (Current) 🚀
**Status**: Foundation ✅ COMPLETE, Ready for User Stories

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
```

### Phase 2: Web Application (Future)
- Add persistent database (PostgreSQL)
- REST API (FastAPI)
- Web UI (Next.js)

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

```bash
# Enter Phase 1 directory
cd phase-1-console/

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run type checking
uv run mypy --strict src/

# Run linting
uv run ruff check src/

# Run the application (when ready)
uv run python -m src.main
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `uv run pytest` | Run all tests |
| `uv run pytest -v` | Verbose test output |
| `uv run mypy --strict src/` | Type check |
| `uv run ruff check src/` | Lint code |
| `uv run python -m src.main` | Run application |

## Contributing

1. Follow TDD: Write tests FIRST
2. Ensure mypy --strict passes
3. Update documentation as you go
4. Create ADRs for architectural decisions
5. One task = one commit

## License

MIT License

---

**Last Updated**: 2025-12-27
**Current Phase**: 1 (Console Application)
**Status**: Foundation Complete, Ready for User Story Implementation
