# Research: TaskFlow Console Application

**Date**: 2025-12-27
**Feature**: Phase 1 Console Application
**Purpose**: Document technology decisions and rationale for implementation

## Research Tasks Completed

### 1. Python Project Structure for CLI Applications

**Decision**: Single flat module structure with separate files for layers

**Rationale**:
- Phase 1 scope is small (~500 LOC) - nested packages would be over-engineering
- Flat structure enables simple imports (`from src.models import Task`)
- Easy to navigate for developers new to the project
- Follows Python convention for small-to-medium projects

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Single file (main.py) | Violates separation of concerns, hard to test |
| Nested packages (src/domain/models/) | Over-engineering for Phase 1 scope |
| No src/ directory | Makes imports messier, harder to package |

### 2. Data Modeling Approach

**Decision**: Python dataclass with `@dataclass` decorator

**Rationale**:
- Built into Python stdlib (no dependencies)
- Automatic `__init__`, `__repr__`, `__eq__` generation
- Type hints are first-class citizens
- Immutable option available via `frozen=True` if needed later
- Works seamlessly with mypy strict mode

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Plain class | More boilerplate, manual __init__ |
| NamedTuple | Less flexible for mutable state (completed toggle) |
| Pydantic BaseModel | External dependency, over-engineering for Phase 1 |
| TypedDict | Less OOP-friendly, no methods |
| attrs library | External dependency |

### 3. Storage Abstraction Pattern

**Decision**: typing.Protocol for interface + concrete InMemoryStorage class

**Rationale**:
- Protocol enables structural subtyping (duck typing with types)
- No inheritance required - any class with matching methods works
- Zero runtime overhead (Protocol is typing-only)
- Enables Phase 2 database backend without changing service layer
- Follows constitution's Evolutionary Architecture principle

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| ABC (Abstract Base Class) | Requires inheritance, more coupling |
| No abstraction | Would require service layer changes in Phase 2 |
| Repository pattern | Over-engineering - we don't need query builders |
| Duck typing without Protocol | Loses type safety benefits |

### 4. Input/Output Handling

**Decision**: Standard input/print with wrapper functions in cli.py

**Rationale**:
- Simplest approach that meets requirements
- Wrapper functions enable testing via mocking
- No external dependencies
- Easy to understand for any Python developer

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| click library | External dependency, CLI args not needed |
| rich library | External dependency, formatting not required |
| argparse | Built-in but for CLI args, not interactive menus |
| curses | Over-complex for simple menu |

### 5. ID Generation Strategy

**Decision**: Sequential integer counter, never reused

**Rationale**:
- Simplest implementation (counter += 1)
- Human-readable IDs (1, 2, 3...)
- No collision risk
- Matches user expectation for small lists
- Constitution requires simplicity over cleverness

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| UUID | Harder to type for users, overkill for in-memory |
| Reuse deleted IDs | Complex tracking, confusing UX |
| Hash-based | Not human-friendly |
| Database auto-increment | No database in Phase 1 |

### 6. Testing Strategy

**Decision**: pytest with fixtures, unit + integration tests

**Rationale**:
- pytest is specified in constitution
- Fixtures enable clean test setup/teardown
- Unit tests for models/services, integration for CLI
- Parameterized tests reduce duplication
- Mocking for input/output in CLI tests

**Test Organization**:
```
tests/
├── unit/           # Fast, isolated tests
│   ├── test_models.py      # Task dataclass behavior
│   ├── test_services.py    # TaskManager methods
│   └── test_storage.py     # InMemoryStorage
└── integration/    # End-to-end flows
    └── test_cli.py         # Menu interactions
```

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| unittest | More verbose, less Pythonic |
| nose2 | Less popular, pytest is standard |
| hypothesis | Property testing is overkill for Phase 1 |

### 7. Error Handling Strategy

**Decision**: Exceptions in service layer, graceful handling in CLI layer

**Rationale**:
- Service layer raises exceptions for invalid operations
- CLI layer catches and displays user-friendly messages
- Clear separation of concerns
- No crashes reach the user

**Exception Flow**:
```
User Input → CLI (validates format) → Service (validates business rules) → Storage
     ↑              ↓                        ↓                              ↓
     └──────────────┴────────────────────────┴──────────────────────────────┘
                    Catch + display friendly message
```

### 8. Timestamp Handling

**Decision**: datetime.now() at task creation, stored but not displayed

**Rationale**:
- Spec requires created_at field
- No display requirement in Phase 1
- Enables future "sort by date" feature
- Python datetime is stdlib, no dependencies

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Unix timestamp | Less readable in debugging |
| String ISO format | Parsing complexity |
| No timestamp | Violates spec requirement FR-003 |
| Third-party (arrow, pendulum) | External dependency |

## Technology Stack Summary

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| Language | Python | 3.13+ | Constitution requirement |
| Package Manager | UV | Latest | Constitution requirement |
| Testing | pytest | Latest | Constitution requirement |
| Type Checking | mypy (strict) | Latest | Constitution requirement |
| Data Model | dataclass | stdlib | No dependencies, type-safe |
| Storage | Protocol + list | stdlib | Simple, extensible |
| CLI | input/print | stdlib | No dependencies needed |

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| How to handle Ctrl+C? | try/except KeyboardInterrupt in main loop |
| Case sensitivity for y/n? | Accept Y/y/N/n (case-insensitive) |
| Empty description allowed? | Yes, optional per spec |
| Max task count? | No hard limit, tested with 1000 |
| What if terminal doesn't support ✓? | Document UTF-8 requirement, no fallback |

## Recommendations for Implementation

1. **Start with models.py** - Establish Task dataclass first
2. **Build storage.py next** - Protocol + InMemoryStorage
3. **Implement services.py** - TaskManager with all CRUD
4. **Create cli.py** - Input/output wrappers
5. **Write main.py last** - Wire everything together

This order ensures each layer is testable independently before integration.
