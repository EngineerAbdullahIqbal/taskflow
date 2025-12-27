# Quality Gates Reference

Detailed documentation for each quality gate.

## Test Gate (pytest)

**Tool**: pytest
**Command**: `uv run pytest -v --tb=short`

### Pass Criteria
- Exit code 0
- All tests pass

### Common Failures
- Test assertions fail
- Fixtures not found
- Import errors

### Quick Fixes
```bash
# Run specific test file
uv run pytest tests/unit/test_models.py -v

# Run with full traceback
uv run pytest --tb=long

# Run last failed tests
uv run pytest --lf
```

## Type Gate (mypy)

**Tool**: mypy --strict
**Command**: `uv run mypy --strict src/`

### Pass Criteria
- Exit code 0
- No type errors

### Strict Mode Rules
- `--disallow-untyped-defs`: All functions must have type hints
- `--disallow-any-explicit`: No `Any` type allowed
- `--warn-return-any`: Warn when returning Any
- `--check-untyped-defs`: Check inside untyped functions

### Common Errors
| Error | Fix |
|-------|-----|
| `Missing return type` | Add `-> ReturnType` |
| `has no attribute` | Check spelling or import |
| `Incompatible types` | Fix type mismatch |
| `Cannot find module` | Add py.typed or stubs |

### Quick Fixes
```bash
# See all errors with context
uv run mypy --strict src/ --show-error-context

# Generate stubs for third-party
uv run stubgen -p package_name
```

## Lint Gate (ruff)

**Tool**: ruff check
**Command**: `uv run ruff check src/`

### Pass Criteria
- Exit code 0
- No violations

### Auto-Fix
```bash
uv run ruff check src/ --fix
```

### Common Rules
| Code | Description |
|------|-------------|
| E501 | Line too long (>88 chars) |
| F401 | Unused import |
| F841 | Unused variable |
| W291 | Trailing whitespace |

### Configuration
Add to `pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "W"]
ignore = ["E501"]  # If needed
```

## Doc Gate (docstrings)

**Tool**: AST parser (built-in)
**Checks**: All public functions/classes have docstrings

### Pass Criteria
- All public functions have docstrings
- All public classes have docstrings

### What Counts as Public
- Functions/classes NOT starting with `_`
- Methods in public classes NOT starting with `_`

### Docstring Format (Google style)
```python
def add_task(title: str, description: str = "") -> Task:
    """Add a new task to the system.

    Args:
        title: The task title (required).
        description: Optional task description.

    Returns:
        The created Task object with assigned ID.

    Raises:
        ValueError: If title is empty.
    """
```

### Quick Fixes
- Add docstrings to listed functions
- Use IDE snippets for consistency
- Run `/tdd-enforcer generate-docs` (if available)
