"""Integration tests for CLI (TDD - Red Phase)."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.cli import (
    get_menu_choice,
    get_task_title,
    get_task_description,
    get_task_id,
    get_confirmation,
    display_tasks,
    display_message,
)
from src.models import Task
from datetime import datetime


# Tests for get_menu_choice

def test_get_menu_choice_valid_1() -> None:
    """Test get_menu_choice accepts valid choice 1."""
    with patch("builtins.input", return_value="1"):
        result = get_menu_choice()
        assert result == 1


def test_get_menu_choice_valid_6() -> None:
    """Test get_menu_choice accepts valid choice 6."""
    with patch("builtins.input", return_value="6"):
        result = get_menu_choice()
        assert result == 6


def test_get_menu_choice_retries_on_invalid() -> None:
    """Test get_menu_choice retries on invalid input."""
    with patch("builtins.input", side_effect=["99", "abc", "3"]):
        with patch("builtins.print"):  # Suppress output
            result = get_menu_choice()
            assert result == 3


# Tests for get_task_title

def test_get_task_title_valid() -> None:
    """Test get_task_title accepts valid title."""
    with patch("builtins.input", return_value="Buy groceries"):
        result = get_task_title()
        assert result == "Buy groceries"


def test_get_task_title_strips_whitespace() -> None:
    """Test get_task_title strips whitespace."""
    with patch("builtins.input", return_value="  Buy groceries  "):
        result = get_task_title()
        assert result == "Buy groceries"


def test_get_task_title_rejects_empty() -> None:
    """Test get_task_title rejects empty input."""
    with patch("builtins.input", side_effect=["", "  ", "Valid title"]):
        with patch("builtins.print"):  # Suppress output
            result = get_task_title()
            assert result == "Valid title"


# Tests for get_task_description

def test_get_task_description_with_input() -> None:
    """Test get_task_description captures input."""
    with patch("builtins.input", return_value="Milk, eggs, bread"):
        result = get_task_description()
        assert result == "Milk, eggs, bread"


def test_get_task_description_empty_allowed() -> None:
    """Test get_task_description allows empty input."""
    with patch("builtins.input", return_value=""):
        result = get_task_description()
        assert result == ""


def test_get_task_description_strips_whitespace() -> None:
    """Test get_task_description strips whitespace."""
    with patch("builtins.input", return_value="  Buy groceries  "):
        result = get_task_description()
        assert result == "Buy groceries"


# Tests for get_task_id

def test_get_task_id_valid() -> None:
    """Test get_task_id accepts valid integer."""
    with patch("builtins.input", return_value="1"):
        result = get_task_id()
        assert result == 1


def test_get_task_id_large_number() -> None:
    """Test get_task_id accepts large numbers."""
    with patch("builtins.input", return_value="999"):
        result = get_task_id()
        assert result == 999


def test_get_task_id_retries_on_non_numeric() -> None:
    """Test get_task_id retries on non-numeric input."""
    with patch("builtins.input", side_effect=["abc", "3.5", "5"]):
        with patch("builtins.print"):  # Suppress output
            result = get_task_id()
            assert result == 5


# Tests for get_confirmation

def test_get_confirmation_yes_lowercase() -> None:
    """Test get_confirmation accepts 'y'."""
    with patch("builtins.input", return_value="y"):
        result = get_confirmation()
        assert result is True


def test_get_confirmation_yes_uppercase() -> None:
    """Test get_confirmation accepts 'Y'."""
    with patch("builtins.input", return_value="Y"):
        result = get_confirmation()
        assert result is True


def test_get_confirmation_no() -> None:
    """Test get_confirmation rejects 'n'."""
    with patch("builtins.input", return_value="n"):
        result = get_confirmation()
        assert result is False


def test_get_confirmation_other_is_no() -> None:
    """Test get_confirmation treats other input as 'no'."""
    with patch("builtins.input", return_value="maybe"):
        result = get_confirmation()
        assert result is False


# Tests for display_tasks

def test_display_tasks_empty() -> None:
    """Test display_tasks shows message for empty list."""
    with patch("builtins.print") as mock_print:
        display_tasks([])
        mock_print.assert_called_with("No tasks found.")


def test_display_tasks_shows_tasks() -> None:
    """Test display_tasks displays all tasks."""
    task1 = Task(id=1, title="Task 1", created_at=datetime.now())
    task2 = Task(id=2, title="Task 2", completed=True, created_at=datetime.now())

    with patch("builtins.print") as mock_print:
        display_tasks([task1, task2])

        # Should print "Your Tasks:" and the tasks
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("Your Tasks:" in str(call) for call in calls)


# Tests for display_message

def test_display_message() -> None:
    """Test display_message prints message."""
    with patch("builtins.print") as mock_print:
        display_message("Test message")
        mock_print.assert_called_once_with("Test message")


# Integration: Full add task flow

def test_add_task_flow_integration() -> None:
    """Test complete add task flow from CLI to service."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())

    # Simulate user input for adding task
    with patch("builtins.input", side_effect=["Buy groceries", "Milk, eggs"]):
        title = get_task_title()
        description = get_task_description()

    task = manager.add_task(title, description)

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs"

    # Verify task is stored
    all_tasks = manager.get_all_tasks()
    assert len(all_tasks) == 1
    assert all_tasks[0].title == "Buy groceries"


def test_view_tasks_flow_integration() -> None:
    """Test complete view tasks flow."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())
    manager.add_task("Task 1")
    manager.add_task("Task 2")

    tasks = manager.get_all_tasks()
    assert len(tasks) == 2

    # Simulate display
    with patch("builtins.print") as mock_print:
        display_tasks(tasks)
        # Verify something was printed
        assert mock_print.called


def test_view_tasks_with_completed_items() -> None:
    """Test viewing tasks shows completion status."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())
    task1 = manager.add_task("Pending Task")
    task2 = manager.add_task("Completed Task")
    manager.toggle_complete(task2.id)

    tasks = manager.get_all_tasks()

    with patch("builtins.print") as mock_print:
        display_tasks(tasks)
        calls = [str(call) for call in mock_print.call_args_list]
        # Verify both tasks are displayed
        task_output = " ".join(calls)
        assert "Pending Task" in task_output
        assert "Completed Task" in task_output


def test_view_tasks_display_format() -> None:
    """Test that displayed tasks show status indicator and ID."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Important Task")

    with patch("builtins.print") as mock_print:
        display_tasks([task])
        call_args = [str(call) for call in mock_print.call_args_list]
        output = " ".join(call_args)
        # Should contain task ID and title
        assert "1" in output
        assert "Important Task" in output


def test_view_empty_tasks_shows_message() -> None:
    """Test viewing empty task list shows appropriate message."""
    with patch("builtins.print") as mock_print:
        display_tasks([])
        mock_print.assert_called_once_with("No tasks found.")


# Tests for mark complete (User Story 3)

def test_mark_complete_flow_integration() -> None:
    """Test complete mark task as complete flow."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Task to complete")

    assert task.completed is False

    # Toggle completion
    completed_task = manager.toggle_complete(task.id)

    assert completed_task is not None
    assert completed_task.completed is True

    # Verify in list
    all_tasks = manager.get_all_tasks()
    assert all_tasks[0].completed is True


def test_mark_complete_with_display() -> None:
    """Test that completed tasks display with checkmark."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Important task")
    manager.toggle_complete(task.id)

    tasks = manager.get_all_tasks()

    with patch("builtins.print") as mock_print:
        display_tasks(tasks)
        calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join(calls)
        # Completed tasks should show checkmark
        assert "[✓]" in output


def test_toggle_back_to_pending() -> None:
    """Test toggling a completed task back to pending."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Toggle task")

    # Mark as complete
    manager.toggle_complete(task.id)
    first_toggle = manager.get_task(task.id)
    assert first_toggle is not None
    assert first_toggle.completed is True

    # Toggle back to pending
    manager.toggle_complete(task.id)
    second_toggle = manager.get_task(task.id)
    assert second_toggle is not None
    assert second_toggle.completed is False


# Tests for delete task (User Story 5)

def test_delete_task_flow_integration() -> None:
    """Test complete delete task flow."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())
    task = manager.add_task("Task to delete")

    # Verify task exists
    assert manager.get_task(task.id) is not None

    # Delete task
    result = manager.delete_task(task.id)

    assert result is True
    assert manager.get_task(task.id) is None


def test_delete_task_with_multiple_tasks() -> None:
    """Test deleting one task from multiple tasks."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())
    manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")
    manager.add_task("Task 3")

    # Delete middle task
    manager.delete_task(task2.id)

    tasks = manager.get_all_tasks()

    assert len(tasks) == 2
    assert task2.id not in [t.id for t in tasks]


def test_delete_nonexistent_task_displays_message() -> None:
    """Test attempting to delete non-existent task."""
    from src.services import TaskManager
    from src.storage import InMemoryStorage

    manager = TaskManager(InMemoryStorage())

    # Try to delete task that doesn't exist
    result = manager.delete_task(999)

    assert result is False
