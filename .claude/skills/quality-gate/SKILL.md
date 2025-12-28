---
name: quality-gate
description: Run all code quality gates (tests, types, lint, docs) and report unified pass/fail status. Use when checking if code is ready to commit, validating before push, running pre-commit checks, or when user says "check quality", "run gates", "validate code", or "/quality-gate". Supports Python projects with UV, pytest, mypy, and ruff.
---

# Quality Gate

Run all constitution-defined quality gates in one command.

## Quick Start

```bash
# Run all gates
uv run python scripts/run_gates.py

# Run with auto-fix for lint issues
uv run python scripts/run_gates.py --fix

# Run specific gate only
uv run python scripts/run_gates.py --gate test
```

## Gates

| Gate | Tool | Pass Criteria |
|------|------|---------------|
| Test | pytest | All tests pass |
| Type | mypy --strict | No type errors |
| Lint | ruff check | No violations |
| Doc | docstring checker | All public functions have docstrings |

## Usage

Execute `scripts/run_gates.py` from project root. See [references/gates.md](references/gates.md) for detailed documentation.

### Output Format

```
╔════════════════════════════════════════════════════════════╗
║                   QUALITY GATE REPORT                      ║
╠════════════════════════════════════════════════════════════╣
║  Gate        │ Status  │ Details                           ║
╠──────────────┼─────────┼───────────────────────────────────╣
║  Test Gate   │ ✅ PASS │ 24/24 tests passed                ║
║  Type Gate   │ ✅ PASS │ No type errors                    ║
║  Lint Gate   │ ⏭ SKIP │ ruff not installed                ║
║  Doc Gate    │ ❌ FAIL │ 3 missing docstrings              ║
╠════════════════════════════════════════════════════════════╣
║  OVERALL     │ ❌ FAIL │ 1 gate failed                     ║
╚════════════════════════════════════════════════════════════╝
```

### Arguments

| Flag | Description |
|------|-------------|
| `--fix` | Auto-fix lint issues with ruff |
| `--gate <name>` | Run single gate: test, type, lint, doc |
| `--strict` | Treat SKIP as FAIL |
| `--src <path>` | Source directory (default: src/) |

### Exit Codes

- **0**: All gates passed
- **1**: One or more gates failed
- **2**: Configuration error
