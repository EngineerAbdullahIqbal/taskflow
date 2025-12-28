"""Tests for TaskManager service layer (TDD - Red Phase)."""

import pytest
from datetime import datetime
from src.models import Task
from src.storage import InMemoryStorage, StorageProtocol


def test_task_manager_initialization() -> None:
    """Test TaskManager accepts StorageProtocol."""
    from src.services import TaskManager

    storage: StorageProtocol = InMemoryStorage()
    manager = TaskManager(storage)

    assert manager is not None


def test_task_manager_with_in_memory_storage() -> None:
    """Test TaskManager works with InMemoryStorage."""
    from src.services import TaskManager

    storage = InMemoryStorage()
    manager = TaskManager(storage)

    assert manager is not None
    assert isinstance(storage, InMemoryStorage)


# Tests for add_task (User Story 1)

def test_add_task_with_title_only() -> None:
    """Test add_task with title and no description."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Buy groceries")

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == ""
    assert task.completed is False


def test_add_task_with_title_and_description() -> None:
    """Test add_task with both title and description."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Buy groceries", "Milk, eggs, bread")

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False


def test_add_task_empty_title_raises_error() -> None:
    """Test add_task raises error for empty title."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())

    with pytest.raises(ValueError, match="Title cannot be empty"):
        manager.add_task("")


def test_add_task_whitespace_title_raises_error() -> None:
    """Test add_task raises error for whitespace-only title."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())

    with pytest.raises(ValueError, match="Title cannot be empty"):
        manager.add_task("   ")


def test_add_task_strips_whitespace() -> None:
    """Test add_task strips leading/trailing whitespace."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("  Buy groceries  ", "  Milk  ")

    assert task.title == "Buy groceries"
    assert task.description == "Milk"


# Tests for get_all_tasks (User Story 2)

def test_get_all_tasks_empty() -> None:
    """Test get_all_tasks returns empty list when no tasks exist."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    tasks = manager.get_all_tasks()

    assert tasks == []


def test_get_all_tasks_returns_all_tasks() -> None:
    """Test get_all_tasks returns all created tasks."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    manager.add_task("Task 3")

    tasks = manager.get_all_tasks()

    assert len(tasks) == 3
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
    assert tasks[2].title == "Task 3"


def test_get_all_tasks_returns_in_creation_order() -> None:
    """Test get_all_tasks returns tasks in creation order."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task1 = manager.add_task("First")
    task2 = manager.add_task("Second")
    task3 = manager.add_task("Third")

    tasks = manager.get_all_tasks()

    assert tasks[0].id == task1.id
    assert tasks[1].id == task2.id
    assert tasks[2].id == task3.id


def test_get_all_tasks_includes_completed_and_pending() -> None:
    """Test get_all_tasks includes both completed and pending tasks."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task1 = manager.add_task("Pending task")
    task2 = manager.add_task("Completed task")
    manager.toggle_complete(task2.id)

    tasks = manager.get_all_tasks()

    assert len(tasks) == 2
    assert tasks[0].completed is False
    assert tasks[1].completed is True


def test_get_all_tasks_does_not_modify_tasks() -> None:
    """Test get_all_tasks does not modify task data."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    original = manager.add_task("Original title", "Original description")

    tasks = manager.get_all_tasks()

    assert tasks[0].title == original.title
    assert tasks[0].description == original.description
    assert tasks[0].completed == original.completed


# Tests for toggle_complete (User Story 3)

def test_toggle_complete_marks_pending_as_completed() -> None:
    """Test toggle_complete marks pending task as completed."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Do something")

    assert task.completed is False

    toggled = manager.toggle_complete(task.id)

    assert toggled is not None
    assert toggled.completed is True


def test_toggle_complete_marks_completed_as_pending() -> None:
    """Test toggle_complete marks completed task back to pending."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Do something")
    manager.toggle_complete(task.id)

    toggled = manager.toggle_complete(task.id)

    assert toggled is not None
    assert toggled.completed is False


def test_toggle_complete_returns_none_for_invalid_id() -> None:
    """Test toggle_complete returns None for non-existent task."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())

    result = manager.toggle_complete(999)

    assert result is None


def test_toggle_complete_persists_changes() -> None:
    """Test toggle_complete persists the change in storage."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Task to complete")
    task_id = task.id

    manager.toggle_complete(task_id)

    # Retrieve the task again
    retrieved = manager.get_task(task_id)

    assert retrieved is not None
    assert retrieved.completed is True


def test_toggle_complete_preserves_other_fields() -> None:
    """Test toggle_complete doesn't modify title, description, etc."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    original = manager.add_task("Original title", "Original description")

    toggled = manager.toggle_complete(original.id)

    assert toggled is not None
    assert toggled.title == original.title
    assert toggled.description == original.description
    assert toggled.id == original.id
    assert toggled.created_at == original.created_at


# Tests for update_task (User Story 4)

def test_update_task_title_only() -> None:
    """Test update_task with new title only."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Original title", "Original description")

    updated = manager.update_task(task.id, title="New title")

    assert updated is not None
    assert updated.title == "New title"
    assert updated.description == "Original description"


def test_update_task_description_only() -> None:
    """Test update_task with new description only."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Title", "Original description")

    updated = manager.update_task(task.id, description="New description")

    assert updated is not None
    assert updated.title == "Title"
    assert updated.description == "New description"


def test_update_task_both_title_and_description() -> None:
    """Test update_task with both title and description."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Original title", "Original description")

    updated = manager.update_task(task.id, title="New title", description="New description")

    assert updated is not None
    assert updated.title == "New title"
    assert updated.description == "New description"


def test_update_task_returns_none_for_invalid_id() -> None:
    """Test update_task returns None for non-existent task."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())

    result = manager.update_task(999, title="New title")

    assert result is None


def test_update_task_preserves_completion_status() -> None:
    """Test update_task doesn't change completion status."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Task")
    manager.toggle_complete(task.id)

    updated = manager.update_task(task.id, title="Updated title")

    assert updated is not None
    assert updated.completed is True


def test_update_task_strips_whitespace() -> None:
    """Test update_task strips whitespace from inputs."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Title")

    updated = manager.update_task(task.id, title="  New title  ", description="  New desc  ")

    assert updated is not None
    assert updated.title == "New title"
    assert updated.description == "New desc"


# Tests for delete_task (User Story 5)

def test_delete_task_removes_task() -> None:
    """Test delete_task removes task from storage."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Task to delete")

    result = manager.delete_task(task.id)

    assert result is True
    assert manager.get_task(task.id) is None


def test_delete_task_returns_false_for_invalid_id() -> None:
    """Test delete_task returns False for non-existent task."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())

    result = manager.delete_task(999)

    assert result is False


def test_delete_task_does_not_affect_other_tasks() -> None:
    """Test delete_task only removes the specified task."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")
    task3 = manager.add_task("Task 3")

    manager.delete_task(task2.id)

    remaining = manager.get_all_tasks()

    assert len(remaining) == 2
    assert remaining[0].id == task1.id
    assert remaining[1].id == task3.id


def test_delete_task_multiple_times_returns_false() -> None:
    """Test deleting same task twice returns False second time."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Task to delete")

    first_delete = manager.delete_task(task.id)
    second_delete = manager.delete_task(task.id)

    assert first_delete is True
    assert second_delete is False


def test_delete_task_id_not_reused() -> None:
    """Test that deleted task IDs are not reused."""
    from src.services import TaskManager

    manager = TaskManager(InMemoryStorage())
    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")

    manager.delete_task(task1.id)

    # Add new task - should get next ID, not reuse deleted ID
    task3 = manager.add_task("Task 3")

    assert task3.id == 3
    assert task3.id != task1.id
