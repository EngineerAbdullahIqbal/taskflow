"""Tests for Task dataclass (TDD - Red Phase)."""

import pytest
from datetime import datetime


def test_task_creation_with_all_fields() -> None:
    """Test Task can be created with all required fields."""
    from src.models import Task

    task = Task(
        id=1,
        title="Buy groceries",
        description="Milk, eggs, bread",
        completed=False,
        created_at=datetime(2025, 12, 27, 10, 30, 0)
    )

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False
    assert task.created_at == datetime(2025, 12, 27, 10, 30, 0)


def test_task_str_format() -> None:
    """Test Task __str__ returns '[status] id. title' format."""
    from src.models import Task

    task_pending = Task(
        id=1,
        title="Buy groceries",
        description="",
        completed=False,
        created_at=datetime.now()
    )

    task_completed = Task(
        id=2,
        title="Call mom",
        description="",
        completed=True,
        created_at=datetime.now()
    )

    assert str(task_pending) == "[ ] 1. Buy groceries"
    assert str(task_completed) == "[✓] 2. Call mom"


def test_task_status_indicator_pending() -> None:
    """Test status_indicator returns '[ ]' for pending task."""
    from src.models import Task

    task = Task(
        id=1,
        title="Test",
        completed=False,
        created_at=datetime.now()
    )

    assert task.status_indicator == "[ ]"


def test_task_status_indicator_completed() -> None:
    """Test status_indicator returns '[✓]' for completed task."""
    from src.models import Task

    task = Task(
        id=1,
        title="Test",
        completed=True,
        created_at=datetime.now()
    )

    assert task.status_indicator == "[✓]"


def test_task_default_values() -> None:
    """Test Task default values for completed and description."""
    from src.models import Task
    from datetime import datetime

    created_time = datetime.now()
    task = Task(id=1, title="Test", created_at=created_time)

    assert task.completed is False
    assert task.description == ""
    assert task.created_at == created_time
