# Quickstart: TaskFlow Console Application

**Date**: 2025-12-27
**Feature**: Phase 1 Console Application
**Audience**: Developers setting up or contributing to TaskFlow

## Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.13+ | `python --version` |
| UV | Latest | `uv --version` |
| Git | Any | `git --version` |

### Installing UV (if not installed)

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### Windows Users: WSL 2 Required

```bash
# Install WSL 2
wsl --install

# Set WSL 2 as default
wsl --set-default-version 2

# Install Ubuntu
wsl --install -d Ubuntu-22.04

# Open Ubuntu terminal and continue from there
```

## Project Setup

### 1. Clone Repository

```bash
git clone https://github.com/EngineerAbdullahIqbal/taskflow.git
cd taskflow

# Switch to Phase 1 branch
git checkout phase-1-console
```

### 2. Initialize Python Project

```bash
# Create virtual environment and install dependencies
uv sync

# This creates:
# - .venv/ directory with Python environment
# - Installs dev dependencies (pytest, mypy)
```

### 3. Verify Setup

```bash
# Check Python version
uv run python --version
# Expected: Python 3.13.x

# Run tests (should pass or show no tests yet)
uv run pytest
# Expected: collected 0 items (initially)

# Check type safety
uv run mypy --strict src/
# Expected: Success (after implementation)
```

## Running the Application

```bash
# Run TaskFlow
uv run python -m src.main

# Or directly
uv run python src/main.py
```

### Expected Output

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

## Development Workflow

### TDD Cycle (Constitution Requirement)

```bash
# 1. Write a failing test
uv run pytest tests/unit/test_models.py -v

# 2. See it fail (RED)
# Expected: FAILED

# 3. Implement the code
# Edit src/models.py

# 4. See it pass (GREEN)
uv run pytest tests/unit/test_models.py -v
# Expected: PASSED

# 5. Refactor if needed

# 6. Check types
uv run mypy --strict src/
```

### Quality Gates

Before committing, run all quality checks:

```bash
# Run all tests
uv run pytest

# Check type safety
uv run mypy --strict src/

# (Optional) Check code style
uv run ruff check src/
```

### Commit Standards

```bash
# Format: type: description
git commit -m "feat: add Task dataclass with validation"
git commit -m "test: add unit tests for TaskManager"
git commit -m "fix: handle empty title validation"
git commit -m "docs: update quickstart with examples"
```

## Project Structure

```
taskflow/
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py            # Entry point
│   ├── cli.py             # User interface
│   ├── models.py          # Task dataclass
│   ├── services.py        # TaskManager
│   └── storage.py         # InMemoryStorage
├── tests/                  # Test files
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_storage.py
│   └── integration/
│       └── test_cli.py
├── specs/                  # Specifications
│   └── phase-1-console/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       └── quickstart.md  # This file
├── .specify/               # SpecifyPlus templates
├── pyproject.toml          # Project configuration
└── README.md               # User documentation
```

## pyproject.toml Configuration

```toml
[project]
name = "taskflow"
version = "0.1.0"
description = "TaskFlow - Intelligent Task Management System"
requires-python = ">=3.13"
dependencies = []

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "mypy>=1.8.0",
]

[tool.mypy]
strict = true
python_version = "3.13"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
```

## Common Tasks

### Adding a New Feature

1. Create failing test in `tests/unit/`
2. Run `uv run pytest` - verify RED
3. Implement in `src/`
4. Run `uv run pytest` - verify GREEN
5. Run `uv run mypy --strict src/`
6. Commit with appropriate type prefix

### Running Specific Tests

```bash
# Run all tests
uv run pytest

# Run specific file
uv run pytest tests/unit/test_models.py

# Run specific test
uv run pytest tests/unit/test_models.py::test_task_creation

# Run with verbose output
uv run pytest -v

# Run with coverage (if installed)
uv run pytest --cov=src
```

### Debugging

```bash
# Run with print output visible
uv run pytest -s

# Run with debugger
uv run python -m pdb src/main.py

# Interactive Python with project context
uv run python -c "from src.models import Task; print(Task)"
```

## Troubleshooting

### UV not found
```bash
# Reload shell or add to PATH
source ~/.bashrc  # or ~/.zshrc
```

### Python version mismatch
```bash
# Install Python 3.13 via UV
uv python install 3.13
```

### Import errors
```bash
# Ensure you're in project root
cd /path/to/taskflow

# Run with module syntax
uv run python -m src.main
```

### Tests not discovered
```bash
# Check test file naming (must start with test_)
ls tests/unit/

# Check function naming (must start with test_)
grep "def test_" tests/unit/test_models.py
```

## Next Steps

1. Read [spec.md](./spec.md) for requirements
2. Read [plan.md](./plan.md) for architecture
3. Read [data-model.md](./data-model.md) for entity details
4. Run `/sp.tasks` to generate implementation tasks
5. Start TDD implementation
