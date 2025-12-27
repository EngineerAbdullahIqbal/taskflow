# Implementation Plan: TaskFlow Console Application

**Branch**: `phase-1-console` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/phase-1-console/spec.md`

## Summary

TaskFlow Phase 1 is a command-line todo application that enables users to manage tasks through an interactive menu-driven interface. The implementation follows a clean three-layer architecture (CLI → Service → Storage) with TDD methodology, full type safety, and in-memory storage. All 5 core CRUD operations (Add, View, Update, Delete, Mark Complete) are delivered via a numbered menu interface.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (stdlib only for runtime; pytest + mypy for development)
**Storage**: In-memory (Python list with sequential ID counter)
**Testing**: pytest with strict TDD (Red-Green-Refactor)
**Target Platform**: Cross-platform terminal/console (Linux, macOS, Windows via WSL)
**Project Type**: Single project (console application)
**Performance Goals**: <2s response for all operations, support 1000+ tasks in memory
**Constraints**: No external runtime dependencies, no persistence, no CLI arguments
**Scale/Scope**: Single user, single session, ~500 LOC estimated

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Test-Driven Development (TDD) - NON-NEGOTIABLE

| Requirement | Plan Compliance | Status |
|-------------|-----------------|--------|
| Tests written BEFORE implementation | All features implemented via Red-Green-Refactor | ✅ PASS |
| pytest as testing framework | pytest configured in pyproject.toml | ✅ PASS |
| Test coverage for public interfaces | Unit tests for TaskManager, integration tests for CLI | ✅ PASS |

### Principle II: Type Safety First

| Requirement | Plan Compliance | Status |
|-------------|-----------------|--------|
| Full type hints on all functions | All functions typed, Task uses dataclass | ✅ PASS |
| Strict mypy configuration | mypy --strict in quality gates | ✅ PASS |
| No Any types | Explicit types only | ✅ PASS |
| Pydantic for validation | Not needed - dataclass sufficient for Phase 1 | ✅ JUSTIFIED |

**Justification for no Pydantic**: Phase 1 has no external input validation boundaries (no API, no file I/O). Simple dataclass with manual validation in service layer is simpler and meets YAGNI principle.

### Principle III: Graceful Degradation

| Requirement | Plan Compliance | Status |
|-------------|-----------------|--------|
| User input errors don't crash | try/except in CLI layer, retry prompts | ✅ PASS |
| User-friendly messages | All error messages specified in FR-012 to FR-015 | ✅ PASS |
| Fallbacks provided | Invalid input prompts retry | ✅ PASS |

### Principle IV: Full Documentation

| Requirement | Plan Compliance | Status |
|-------------|-----------------|--------|
| Docstrings on public functions | Required in code standards | ✅ PASS |
| Module README | README.md in project root | ✅ PASS |
| Architecture in specs/ | plan.md, data-model.md, research.md | ✅ PASS |

### Principle V: Evolutionary Architecture

| Requirement | Plan Compliance | Status |
|-------------|-----------------|--------|
| Phase 1 prioritizes simplicity | Minimal abstractions, stdlib only | ✅ PASS |
| Protocols for components that change | StorageProtocol for future database | ✅ PASS |
| CLI → Service → Storage separation | Three distinct layers | ✅ PASS |
| Minimal dependencies | Zero runtime deps | ✅ PASS |

### Principle VI: Simplicity & YAGNI

| Requirement | Plan Compliance | Status |
|-------------|-----------------|--------|
| Simplest solution | List-based storage, no ORM | ✅ PASS |
| No premature optimization | Simple iteration, no caching | ✅ PASS |
| No features beyond scope | Only 5 CRUD operations | ✅ PASS |

**CONSTITUTION CHECK RESULT**: ✅ ALL GATES PASSED

## Project Structure

### Documentation (this feature)

```text
specs/phase-1-console/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Technology decisions and rationale
├── data-model.md        # Entity definitions and relationships
├── quickstart.md        # Developer setup instructions
├── checklists/
│   └── requirements.md  # Spec quality validation
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── main.py              # Entry point, main loop
├── cli.py               # Menu display, user input handling
├── models.py            # Task dataclass definition
├── services.py          # TaskManager business logic
└── storage.py           # StorageProtocol + InMemoryStorage

tests/
├── __init__.py
├── conftest.py          # Shared fixtures (TaskManager, sample tasks)
├── unit/
│   ├── __init__.py
│   ├── test_models.py   # Task dataclass tests
│   ├── test_services.py # TaskManager method tests
│   └── test_storage.py  # Storage implementation tests
└── integration/
    ├── __init__.py
    └── test_cli.py      # End-to-end menu flow tests
```

**Structure Decision**: Single project structure selected. Clean separation achieved through modules rather than packages. The `storage.py` module contains a Protocol to enable future database backends while keeping Phase 1 simple.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Layer (cli.py)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ display_menu│  │ get_input   │  │ format_task_display     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ calls
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Service Layer (services.py)                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      TaskManager                             ││
│  │  • add_task(title, description) → Task                      ││
│  │  • get_all_tasks() → list[Task]                             ││
│  │  • get_task(id) → Task | None                               ││
│  │  • update_task(id, title, description) → Task | None        ││
│  │  • delete_task(id) → bool                                   ││
│  │  • toggle_complete(id) → Task | None                        ││
│  └─────────────────────────────────────────────────────────────┘│
└──────────────────────────────┬──────────────────────────────────┘
                               │ uses
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Storage Layer (storage.py)                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              StorageProtocol (abstract)                      ││
│  │  • add(task) → Task                                         ││
│  │  • get_all() → list[Task]                                   ││
│  │  • get(id) → Task | None                                    ││
│  │  • update(task) → Task                                      ││
│  │  • delete(id) → bool                                        ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              InMemoryStorage (implementation)                ││
│  │  • tasks: list[Task]                                        ││
│  │  • next_id: int                                             ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### main.py
- Application entry point
- Creates TaskManager with InMemoryStorage
- Runs main loop until exit
- Handles Ctrl+C gracefully

### cli.py
- `display_menu()`: Prints menu to stdout
- `get_menu_choice()`: Reads and validates 1-6 input
- `get_task_id()`: Reads and validates integer ID
- `get_task_title()`: Reads and validates non-empty title
- `get_task_description()`: Reads optional description
- `get_confirmation()`: Reads y/n for delete
- `display_tasks(tasks)`: Formats and prints task list
- `display_message(msg)`: Prints feedback messages

### models.py
- `Task` dataclass with id, title, description, completed, created_at
- `__str__` method for display formatting

### services.py
- `TaskManager` class with CRUD operations
- Validates business rules (non-empty title, ID exists)
- Delegates storage to injected StorageProtocol

### storage.py
- `StorageProtocol` (typing.Protocol) defines interface
- `InMemoryStorage` implements with list + counter

## Complexity Tracking

> No violations to justify - all constitution requirements met with simple solutions.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| No Pydantic | Use dataclass | No API boundaries in Phase 1 |
| No Repository pattern | Direct list operations | Only one storage type in Phase 1 |
| Protocol for storage | Enable Phase 2 database | Minimal overhead, high value |

## Quality Gates (from Constitution)

All code must pass before merge:

1. **Test Gate**: `pytest` - all tests pass
2. **Type Gate**: `mypy --strict src/` - no type errors
3. **Lint Gate**: `ruff check src/` - no lint violations (optional for Phase 1)
4. **Doc Gate**: All public functions have docstrings
5. **Review Gate**: AI partner review via Claude Code

## Development Workflow

1. **Setup**: `uv init` + `uv add --dev pytest mypy`
2. **TDD Cycle** for each feature:
   - Write failing test
   - Run `pytest` (RED)
   - Implement minimal code
   - Run `pytest` (GREEN)
   - Refactor if needed
   - Run `mypy --strict`
3. **Commit**: Atomic commits per feature
4. **Quality Gates**: Run before push

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| UTF-8 checkmark not displaying | Low | Low | Fallback to [x] if needed |
| Python 3.13 not available | Low | High | Document 3.12+ as minimum |
| pytest fixtures complexity | Low | Low | Keep fixtures minimal |

## Next Steps

1. Run `/sp.tasks` to generate implementation task breakdown
2. Execute tasks using TDD methodology
3. Validate against quality gates
4. Create PR to phase-1-console branch (if on feature branch)
