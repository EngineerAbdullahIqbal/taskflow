---
name: tdd-enforcer
description: Enforce Test-Driven Development workflow by detecting missing tests, generating test templates, and validating Red-Green-Refactor cycle. Use when implementing features, writing code, checking TDD compliance, or when user says "check tdd", "generate tests", "enforce tests", or "/tdd-enforcer". Essential for constitution-compliant development.
---

# TDD Enforcer

Enforce Test-Driven Development (TDD) as required by the TaskFlow Constitution.

## Quick Start

```bash
# Check if code has corresponding tests
uv run python scripts/tdd_check.py src/

# Generate test template for a module
uv run python scripts/generate_tests.py src/services.py

# Validate TDD compliance (strict mode)
uv run python scripts/tdd_check.py --strict src/
```

## Core Functions

| Function | Description |
|----------|-------------|
| Check | Detect code without corresponding tests |
| Generate | Create test file templates from source |
| Validate | Ensure tests written before implementation |

## Usage

### Check TDD Compliance

```bash
uv run python scripts/tdd_check.py src/
```

Output:
```
TDD Compliance Report
═════════════════════════════════════════════════════
Module              │ Functions │ Tested │ Status
────────────────────┼───────────┼────────┼─────────
src/models.py       │ 3         │ 3      │ ✅ PASS
src/services.py     │ 6         │ 4      │ ❌ FAIL
src/cli.py          │ 5         │ 0      │ ❌ FAIL
═════════════════════════════════════════════════════
Overall: 14 functions, 7 tested (50%)

Missing tests:
  src/services.py:
    - update_task (line 45)
    - delete_task (line 62)
```

### Generate Test Templates

```bash
uv run python scripts/generate_tests.py src/services.py
```

Creates test file with stubs for all public functions.

### Strict Mode

```bash
uv run python scripts/tdd_check.py --strict src/
```

Exit code 1 if ANY function lacks a test. Use in CI/CD to block PRs.

## TDD Workflow

```
1. RED    → Write failing test first
2. GREEN  → Write minimal code to pass
3. REFACTOR → Improve code, keep tests green
```

## Arguments

| Flag | Description |
|------|-------------|
| `--strict` | Exit with error if any function untested |
| `--generate` | Auto-generate missing test files |
| `--tests <path>` | Test directory (default: tests/) |

## References

See [references/tdd_patterns.md](references/tdd_patterns.md) for TDD best practices.
