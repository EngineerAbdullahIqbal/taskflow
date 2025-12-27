# Scaffold Templates

Templates used by the python-scaffold skill.

## Module Template

```python
"""
{name} module.

Provides {name} functionality.
"""

from typing import Optional

__all__: list[str] = []
```

## Service Template

```python
"""
{name_title} Service implementation.

Handles {name} business logic.
"""

from typing import Optional

from .protocols import {name_title}Protocol


class {name_title}Service:
    """Implementation of {name_title}Protocol."""

    def __init__(self) -> None:
        """Initialize the service."""
        pass
```

## Protocol Template

```python
"""
Service protocols (interfaces).

Define abstract interfaces for dependency injection.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class {name_title}Protocol(Protocol):
    """Interface for {name} operations."""

    pass
```

## Test Template

```python
"""
Tests for {name} module.

Following TDD: Write tests FIRST.
"""

import pytest


class Test{name_title}:
    """Tests for {name} module."""

    def test_placeholder(self) -> None:
        """TODO: Replace with actual tests."""
        # Arrange

        # Act

        # Assert
        assert True  # TODO: Add real assertion
```

## Customization

To customize templates:
1. Copy this file to your project
2. Modify templates as needed
3. Pass `--template-dir` to scaffold.py

## Naming Conventions

| Input | Module Name | Class Name |
|-------|-------------|------------|
| `task` | `task.py` | `TaskService` |
| `task_manager` | `task_manager.py` | `TaskManagerService` |
| `user_auth` | `user_auth.py` | `UserAuthService` |
