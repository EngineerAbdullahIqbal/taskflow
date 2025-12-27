# TaskFlow - Intelligent Task Management System (Phase 1)

A command-line todo application written in Python with an interactive menu-driven interface.

## Features

- ✨ **Add Tasks**: Create tasks with title and optional description
- 👀 **View Tasks**: See all your tasks with completion status
- ✅ **Mark Complete**: Toggle task completion status
- ✏️ **Update Tasks**: Modify task title and description
- 🗑️ **Delete Tasks**: Remove tasks from your list
- 🚪 **Exit Gracefully**: Clean exit with save confirmation

## Quick Start

### Prerequisites

- Python 3.13+
- UV package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/EngineerAbdullahIqbal/taskflow.git
cd taskflow

# Install dependencies
uv sync
```

### Running the Application

```bash
# Run with UV
uv run python -m src.main

# Or activate virtual environment
source .venv/bin/activate
python -m src.main
```

## Usage

The application presents an interactive menu:

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

Follow the on-screen prompts to manage your tasks.

## Architecture

TaskFlow follows a clean three-layer architecture:

```
CLI Layer (cli.py)
    ↓
Service Layer (services.py)
    ↓
Storage Layer (storage.py)
```

### Key Components

- **models.py**: Task dataclass with validation
- **services.py**: TaskManager business logic
- **storage.py**: StorageProtocol and InMemoryStorage
- **cli.py**: User interface and input handling
- **main.py**: Application entry point

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/unit/test_models.py
```

### Type Checking

```bash
# Check types with mypy strict mode
uv run mypy --strict src/
```

### Linting

```bash
# Check code style
uv run ruff check src/

# Fix code style issues
uv run ruff check --fix src/
```

### Quality Gates

All code must pass these gates before merge:

1. **Tests**: `uv run pytest` - all tests pass
2. **Types**: `uv run mypy --strict src/` - no type errors
3. **Lint**: `uv run ruff check src/` - no violations
4. **Docs**: All public functions have docstrings

## Design Decisions

See [ADR-001](history/adr/ADR-001-three-layer-architecture-with-protocol-abstraction.md) and [ADR-002](history/adr/ADR-002-data-modeling-with-dataclass-and-validation.md) for architecture decisions.

## Roadmap

- **Phase 1**: In-memory console application (current)
- **Phase 2**: Add persistence and web interface
- **Phase 3**: Add AI-powered features
- **Phase 4**: Deploy to cloud
- **Phase 5**: Collaborative features

## License

MIT License

## Authors

Abdullah Iqbal - Engineer

---

**Note**: Phase 1 stores all data in memory. Data is lost when the application exits.
