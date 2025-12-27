<!--
  ============================================================================
  SYNC IMPACT REPORT
  ============================================================================
  Version Change: 1.0.0 → 1.1.0 (branching strategy added)

  Modified Principles:
    - None

  Added Sections:
    - Branching Strategy (phase-based branch structure and rules)

  Removed Sections:
    - None

  Templates Status:
    - .specify/templates/plan-template.md ✅ Compatible
    - .specify/templates/spec-template.md ✅ Compatible
    - .specify/templates/tasks-template.md ✅ Compatible

  Follow-up TODOs:
    - Create phase-1-console branch
    - Configure GitHub remote if not present
  ============================================================================
-->

# TaskFlow Constitution

## Core Principles

### I. Test-Driven Development (TDD) - NON-NEGOTIABLE

Test-Driven Development is mandatory for all feature development. This principle ensures code correctness, enables safe refactoring, and serves as living documentation.

- Tests MUST be written BEFORE implementation code
- Red-Green-Refactor cycle MUST be strictly enforced:
  1. **Red**: Write a failing test that defines expected behavior
  2. **Green**: Write minimal code to make the test pass
  3. **Refactor**: Improve code quality while keeping tests green
- No code merges are permitted without passing tests
- pytest is the designated testing framework
- Test coverage MUST be maintained for all public interfaces

**Rationale**: TDD catches bugs early, forces clear API design, and provides confidence for future changes. Skipping tests creates technical debt that compounds over time.

### II. Type Safety First

Static typing prevents entire categories of runtime errors and improves code maintainability. TypeScript-style strictness applies to Python.

- Full type hints MUST be present on all functions, methods, and class attributes
- Strict mypy configuration MUST be enforced (no `Any` types allowed except in rare, documented cases)
- Pydantic models MUST be used for data validation at system boundaries
- Type errors are build failures and MUST block merges
- Generic types MUST be used appropriately (e.g., `list[Task]` not `list`)

**Rationale**: Type safety enables IDE support, catches errors at development time, and serves as executable documentation that cannot become stale.

### III. Graceful Degradation

The system MUST handle errors gracefully, providing meaningful feedback to users while maintaining stability.

- User input errors MUST NOT crash the application
- Internal errors MUST be logged with full context for debugging
- User-facing messages MUST be friendly and actionable (no stack traces)
- Fallbacks MUST be provided where possible (e.g., invalid input prompts retry)
- Error boundaries MUST isolate failures to prevent cascade effects

**Rationale**: Users should never see a crash or cryptic error. Professional software handles edge cases gracefully and guides users toward success.

### IV. Full Documentation

Documentation is a first-class deliverable, not an afterthought. Code without documentation is incomplete.

- Docstrings MUST be present on all public functions, classes, and modules
- Each module MUST have a README explaining its purpose and usage
- Architecture decisions MUST be documented in `specs/` folder
- Documentation MUST be updated synchronously with code changes
- Examples MUST be provided for complex interfaces

**Rationale**: Documentation enables team scaling, reduces onboarding time, and prevents knowledge silos. Self-documenting code is a myth.

### V. Evolutionary Architecture

Design for today's requirements while enabling tomorrow's growth. Use abstractions strategically.

- Phase 1 MUST prioritize simplicity over future-proofing
- Interfaces/Protocols MUST be used for components that will change (e.g., storage)
- Clean layer separation MUST be maintained: CLI → Service → Storage
- Minimal dependencies MUST be preferred; stdlib over third-party when equivalent
- Abstractions MUST be justified by actual (not hypothetical) requirements

**Rationale**: Over-engineering is as harmful as under-engineering. The right abstraction emerges from concrete use cases, not speculation.

### VI. Simplicity & YAGNI

Start with the smallest viable implementation. Add complexity only when requirements demand it.

- Implement the simplest solution that satisfies current requirements
- No premature optimization (profile first, optimize second)
- No features beyond current phase scope
- Three similar lines of code are better than one premature abstraction
- Delete dead code immediately; do not comment it out

**Rationale**: Complexity is the enemy of reliability. Every line of code is a liability. Simple systems are easier to understand, test, and maintain.

## Phase 1 Constraints

This section defines the technology boundaries and scope limits for Phase 1 (Console Application).

### Technology Stack

| Component | Requirement |
|-----------|-------------|
| Language | Python 3.13+ |
| Package Manager | UV (Astral) |
| Testing Framework | pytest |
| Type Checking | mypy (strict mode) |
| External Dependencies | stdlib + pytest only |

### Scope Boundaries

**In Scope (Phase 1)**:
- Task entity: `id`, `title`, `description`, `completed`, `created_at`
- Interactive menu-driven CLI (numbered menu 1-6)
- CRUD operations: Add, View, Update, Delete, Mark Complete
- Pure in-memory storage (tasks lost on exit)

**Explicitly Out of Scope (Phase 1)**:
- Command-line arguments
- File persistence or database
- Priority levels or due dates
- Categories or tags
- Search or filtering
- User authentication

### CLI Specification

The CLI MUST follow this interaction pattern:
```
=== TaskFlow ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Exit

Enter choice (1-6): _
```

## Branching Strategy

TaskFlow uses a phase-based branching strategy to support incremental evolution across 5 phases.

### Branch Structure

| Branch | Purpose | Base |
|--------|---------|------|
| `master` | Production-ready code, constitution, shared artifacts | - |
| `phase-1-console` | Phase 1: Python console application | master |
| `phase-2-fullstack` | Phase 2: Next.js + FastAPI + PostgreSQL | phase-1-console |
| `phase-3-ai-chatbot` | Phase 3: AI chatbot with MCP + OpenAI Agents | phase-2-fullstack |
| `phase-4-kubernetes` | Phase 4: Local Kubernetes with Minikube | phase-3-ai-chatbot |
| `phase-5-cloud` | Phase 5: Cloud deployment with Kafka + Dapr | phase-4-kubernetes |

### Branch Rules

- Each phase branch MUST be created from its predecessor
- Phase branches MUST NOT be deleted after creation
- Work on a phase MUST happen on that phase's branch
- Feature branches within a phase follow pattern: `phase-N/<feature-name>`
- PRs within a phase target that phase's branch
- Phase completion triggers PR to next phase branch (or master for phase-5)

### Workflow

```
master (constitution, shared docs)
  └── phase-1-console
        └── phase-1/add-task-feature
        └── phase-1/view-tasks-feature
        └── ...
  └── phase-2-fullstack (created after phase-1 complete)
        └── phase-2/api-endpoints
        └── ...
```

## Development Workflow

### Quality Gates

All code MUST pass these gates before merge:

1. **Test Gate**: All tests pass (`pytest`)
2. **Type Gate**: No type errors (`mypy --strict`)
3. **Lint Gate**: Code follows style guidelines
4. **Doc Gate**: Public interfaces have docstrings
5. **Review Gate**: Code reviewed by AI partner or human

### Review Process

1. Create feature branch from `master`
2. Implement using TDD (Red-Green-Refactor)
3. Run quality gates locally before commit
4. Create PR with description of changes
5. Address review feedback
6. Merge after all gates pass

### Commit Standards

- Commits MUST be atomic (one logical change per commit)
- Commit messages MUST follow format: `type: description`
- Types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`
- Description MUST be imperative mood ("add" not "added")

## Governance

This constitution is the supreme authority for TaskFlow development. All code, designs, and decisions MUST comply with these principles.

### Amendment Process

1. Propose amendment with rationale
2. Document impact on existing code
3. Obtain approval from project owner
4. Update constitution with new version
5. Migrate non-compliant code (if any)

### Versioning Policy

Constitution follows semantic versioning:
- **MAJOR**: Principle removal or backward-incompatible redefinition
- **MINOR**: New principle added or existing principle materially expanded
- **PATCH**: Clarifications, typos, non-semantic refinements

### Compliance Review

- All PRs MUST verify compliance with constitution
- Non-compliance MUST be documented with justification
- Unjustified violations MUST block merge
- Periodic audits SHOULD verify ongoing compliance

**Version**: 1.1.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
