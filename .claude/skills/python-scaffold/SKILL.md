---
name: python-scaffold
description: Generate standardized Python project scaffolding following constitution patterns. Use when creating new modules, services, or project structure. Triggers on "scaffold", "create module", "new service", "init python", "/python-scaffold". Enforces type hints, docstrings, and test structure.
---

# Python Scaffold

Generate constitution-compliant Python project structure.

## Quick Start

```bash
# Create new module with tests
uv run python scripts/scaffold.py module models

# Create service layer
uv run python scripts/scaffold.py service task

# Create full project structure
uv run python scripts/scaffold.py project src/
```

## Commands

| Command | Description |
|---------|-------------|
| `module <name>` | Create module with `__init__.py`, types, tests |
| `service <name>` | Create service class with interface, impl, tests |
| `project <path>` | Create full directory structure |

## Generated Structure

### Module
```
src/
├── <name>.py          # Implementation with type hints
├── __init__.py        # Exports
tests/
├── unit/
│   └── test_<name>.py # Test stubs
```

### Service
```
src/
├── services/
│   ├── __init__.py
│   ├── <name>_service.py    # Service implementation
│   └── protocols.py         # Service protocol/interface
tests/
├── unit/
│   └── test_<name>_service.py
```

## Features

- Full type hints (mypy strict compatible)
- Docstrings on all public functions
- Arrange-Act-Assert test templates
- Protocol-based interfaces for services
- `__all__` exports in `__init__.py`

## Arguments

| Flag | Description |
|------|-------------|
| `--dry-run` | Show what would be created |
| `--force` | Overwrite existing files |
| `--no-tests` | Skip test file generation |

## Templates

See [references/templates.md](references/templates.md) for customizable templates.
