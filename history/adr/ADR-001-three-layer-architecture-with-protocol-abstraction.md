# ADR-001: Three-Layer Architecture with Protocol Abstraction

> **Scope**: Clustered decision covering application structure, layer separation, and storage abstraction strategy for TaskFlow Phase 1 and beyond.

- **Status:** Accepted
- **Date:** 2025-12-27
- **Feature:** phase-1-console
- **Context:** TaskFlow requires a foundation that supports Phase 1 simplicity (in-memory, console) while enabling evolution to Phase 2+ (database, web API). The architecture must balance YAGNI principles with extensibility.

## Decision

Adopt a three-layer architecture with Protocol-based storage abstraction:

**Layer Structure:**
- **CLI Layer** (`cli.py`): User interface, input validation, display formatting
- **Service Layer** (`services.py`): Business logic, CRUD operations via TaskManager
- **Storage Layer** (`storage.py`): Data persistence via StorageProtocol + InMemoryStorage

**Abstraction Strategy:**
- **Interface**: `typing.Protocol` (structural subtyping, zero runtime overhead)
- **Phase 1 Implementation**: `InMemoryStorage` (Python list + sequential ID counter)
- **Future Implementations**: `PostgresStorage`, `SQLiteStorage` (same Protocol, no service changes)

**Dependency Direction:**
```
CLI → Service → Storage (Protocol)
                    ↑
              InMemoryStorage
```

## Consequences

### Positive

1. **Clean Separation**: Each layer has single responsibility, testable in isolation
2. **Evolutionary Ready**: Phase 2 database requires only new Storage class, no service changes
3. **Type Safe**: Protocol provides compile-time interface verification via mypy
4. **Zero Overhead**: Protocol is typing-only, no runtime inheritance cost
5. **TDD Friendly**: Service layer tested with mock storage, CLI tested with mock input/output
6. **Constitution Compliant**: Meets Principle V (Evolutionary Architecture) and VI (Simplicity)

### Negative

1. **Indirection Cost**: Three files instead of one, more imports to navigate
2. **Protocol Learning Curve**: Less familiar than ABC for some Python developers
3. **Over-Design Risk**: For Phase 1 alone, direct list access would be simpler
4. **Testing Fixtures**: Need storage fixtures for service tests (minor overhead)

## Alternatives Considered

### Alternative A: Single Module (Monolith)
All code in `main.py` with direct list manipulation.

**Rejected because:**
- Violates separation of concerns (constitution requirement)
- Cannot test business logic without testing UI
- Any future change requires rewriting entire file
- Fails TDD isolation requirements

### Alternative B: ABC (Abstract Base Class) for Storage
Use `abc.ABC` + `@abstractmethod` instead of Protocol.

**Rejected because:**
- Requires inheritance (`class InMemoryStorage(StorageABC)`)
- More coupling between interface and implementation
- Protocol's structural subtyping is more Pythonic
- ABC adds runtime overhead (descriptor protocol)

### Alternative C: No Abstraction (Direct InMemoryStorage)
TaskManager uses InMemoryStorage directly without Protocol.

**Rejected because:**
- Phase 2 database integration requires TaskManager code changes
- Violates Evolutionary Architecture principle
- Minimal upfront cost for Protocol justifies future savings

### Alternative D: Repository Pattern
Full Repository pattern with query builder abstraction.

**Rejected because:**
- Over-engineering for Phase 1 (YAGNI violation)
- No complex queries needed (only CRUD + list all)
- Protocol provides sufficient abstraction
- Can evolve to Repository if Phase 3+ needs complex queries

## References

- Feature Spec: [specs/phase-1-console/spec.md](../../specs/phase-1-console/spec.md)
- Implementation Plan: [specs/phase-1-console/plan.md](../../specs/phase-1-console/plan.md)
- Research Notes: [specs/phase-1-console/research.md](../../specs/phase-1-console/research.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Principles V, VI)
- Related ADRs: ADR-002 (Data Modeling Approach)
