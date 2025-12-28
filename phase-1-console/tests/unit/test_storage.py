"""Tests for StorageProtocol and InMemoryStorage (TDD - Red Phase)."""

import pytest
from datetime import datetime
from src.models import Task


def test_storage_add_returns_task_with_id() -> None:
    """Test storage.add() returns Task with assigned ID."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    task = Task(
        id=0,  # Placeholder
        title="Test task",
        created_at=datetime.now()
    )

    result = storage.add(task)
    assert result.id == 1
    assert result.title == "Test task"


def test_storage_get_all_empty() -> None:
    """Test storage.get_all() returns empty list initially."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    assert storage.get_all() == []


def test_storage_get_all_returns_all_tasks() -> None:
    """Test storage.get_all() returns all added tasks."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    task1 = Task(id=0, title="Task 1", created_at=datetime.now())
    task2 = Task(id=0, title="Task 2", created_at=datetime.now())

    storage.add(task1)
    storage.add(task2)

    tasks = storage.get_all()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_storage_get_by_id_returns_task() -> None:
    """Test storage.get(id) returns Task when found."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    task = Task(id=0, title="Test task", created_at=datetime.now())
    added = storage.add(task)

    result = storage.get(added.id)
    assert result is not None
    assert result.title == "Test task"


def test_storage_get_by_id_returns_none() -> None:
    """Test storage.get(id) returns None when not found."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    result = storage.get(999)
    assert result is None


def test_storage_update_modifies_task() -> None:
    """Test storage.update() modifies existing task."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    task = Task(id=0, title="Original", created_at=datetime.now())
    added = storage.add(task)

    updated = Task(
        id=added.id,
        title="Updated",
        created_at=added.created_at
    )

    result = storage.update(updated)
    assert result.title == "Updated"

    retrieved = storage.get(added.id)
    assert retrieved.title == "Updated"


def test_storage_delete_returns_true() -> None:
    """Test storage.delete(id) returns True when found."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    task = Task(id=0, title="Test", created_at=datetime.now())
    added = storage.add(task)

    result = storage.delete(added.id)
    assert result is True


def test_storage_delete_returns_false() -> None:
    """Test storage.delete(id) returns False when not found."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    result = storage.delete(999)
    assert result is False


def test_storage_delete_removes_task() -> None:
    """Test storage.delete() removes task from storage."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    task = Task(id=0, title="Test", created_at=datetime.now())
    added = storage.add(task)

    storage.delete(added.id)
    result = storage.get(added.id)
    assert result is None


def test_storage_sequential_id_generation() -> None:
    """Test sequential ID generation (1, 2, 3...)."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    task1 = Task(id=0, title="Task 1", created_at=datetime.now())
    task2 = Task(id=0, title="Task 2", created_at=datetime.now())
    task3 = Task(id=0, title="Task 3", created_at=datetime.now())

    result1 = storage.add(task1)
    result2 = storage.add(task2)
    result3 = storage.add(task3)

    assert result1.id == 1
    assert result2.id == 2
    assert result3.id == 3


def test_storage_ids_never_reused() -> None:
    """Test IDs are never reused after deletion."""
    from src.storage import InMemoryStorage

    storage = InMemoryStorage()
    task1 = Task(id=0, title="Task 1", created_at=datetime.now())
    task2 = Task(id=0, title="Task 2", created_at=datetime.now())
    task3 = Task(id=0, title="Task 3", created_at=datetime.now())

    t1 = storage.add(task1)  # ID 1
    t2 = storage.add(task2)  # ID 2
    t3 = storage.add(task3)  # ID 3

    storage.delete(t1.id)  # Delete ID 1

    task4 = Task(id=0, title="Task 4", created_at=datetime.now())
    t4 = storage.add(task4)

    assert t4.id == 4  # Should be 4, not reused 1
