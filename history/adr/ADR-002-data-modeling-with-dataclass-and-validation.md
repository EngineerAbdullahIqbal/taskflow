# ADR-002: Data Modeling with Dataclass and Service-Layer Validation

> **Scope**: Clustered decision covering Task entity design, data modeling approach, and validation strategy for TaskFlow Phase 1 and future phases.

- **Status:** Accepted
- **Date:** 2025-12-27
- **Feature:** phase-1-console
- **Context:** TaskFlow needs a Task entity that is type-safe, simple for Phase 1, and can evolve to support API validation in Phase 2+. The choice of data modeling affects testing, serialization, and future database mapping.

## Decision

Use Python's built-in `dataclass` with service-layer validation:

**Entity Definition:**
- **Task** dataclass with 5 fields: `id`, `title`, `description`, `completed`, `created_at`
- Immutability: Not frozen (Task.completed needs toggle)
- Defaults: `description=""`, `completed=False`, `created_at=datetime.now()`

**Validation Strategy:**
- **Phase 1**: Validation in TaskManager service layer (not in dataclass)
- **Validation Rules**: VR-001 to VR-004 (non-empty title, length limits)
- **Error Handling**: Raise exceptions in service, catch in CLI

**Type Annotations:**
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

## Consequences

### Positive

1. **Zero Dependencies**: dataclass is Python stdlib, no pip install required
2. **Type Safety**: Full mypy --strict compatibility, type hints first-class
3. **Simplicity**: Auto-generated `__init__`, `__repr__`, `__eq__`
4. **TDD Friendly**: Easy to construct test instances with keyword args
5. **Constitution Compliant**: Meets Principle II (Type Safety) and VI (Simplicity)
6. **Future Ready**: Can add `__post_init__` validation or migrate to Pydantic later

### Negative

1. **No Built-in Validation**: Validation logic in service layer, not declarative
2. **No Serialization**: Manual dict conversion needed for Phase 2 API
3. **Mutable Default Risk**: Must use `field(default_factory=)` for datetime
4. **Evolution Overhead**: Phase 2 may require migration to Pydantic for API validation

## Alternatives Considered

### Alternative A: Pydantic BaseModel
Use Pydantic for declarative validation and serialization.

**Rejected because:**
- External dependency violates "minimal dependencies" constitution principle
- No API boundary in Phase 1 (no JSON serialization needed)
- Over-engineering for in-memory console app
- Validation in service layer is simpler for Phase 1

**Reconsidered for Phase 2**: When API is introduced, Pydantic becomes justified for request/response validation.

### Alternative B: NamedTuple
Use `typing.NamedTuple` for immutable data structure.

**Rejected because:**
- Task.completed requires mutation (toggle complete)
- Would need to replace entire tuple on each change
- Less flexible than dataclass for adding methods

### Alternative C: TypedDict
Use TypedDict for dictionary-based data with types.

**Rejected because:**
- Less OOP-friendly (no methods on dicts)
- No constructor validation
- Harder to work with in service layer
- Dictionary access less readable than attribute access

### Alternative D: Plain Class with Manual __init__
Traditional Python class with manual property definitions.

**Rejected because:**
- More boilerplate (10+ lines vs 5 with dataclass)
- No auto-generated `__eq__`, `__repr__`
- dataclass is the modern Python idiom

### Alternative E: attrs Library
Use attrs for feature-rich dataclass alternative.

**Rejected because:**
- External dependency
- dataclass is sufficient for Phase 1 needs
- attrs benefits (converters, validators) not needed yet

## Validation Design

| Layer | Responsibility | Example |
|-------|---------------|---------|
| CLI | Format validation | "Is input a valid integer?" |
| Service | Business validation | "Is title non-empty?" |
| Storage | None | Trusts service layer |

```python
# Service layer validation (in TaskManager)
def add_task(self, title: str, description: str = "") -> Task:
    if not title.strip():
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title must be 1-200 characters")
    # ... create task
```

## Evolution Path

| Phase | Change | Migration Effort |
|-------|--------|-----------------|
| Phase 2 | Add Pydantic for API schemas | Create separate `TaskCreate`, `TaskResponse` models |
| Phase 2 | Database mapping | Add SQLAlchemy model, keep dataclass for domain |
| Phase 3 | Add fields (priority, due_date) | Simple dataclass field addition |

## References

- Feature Spec: [specs/phase-1-console/spec.md](../../specs/phase-1-console/spec.md)
- Data Model: [specs/phase-1-console/data-model.md](../../specs/phase-1-console/data-model.md)
- Research Notes: [specs/phase-1-console/research.md](../../specs/phase-1-console/research.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Principles II, VI)
- Related ADRs: ADR-001 (Three-Layer Architecture)
