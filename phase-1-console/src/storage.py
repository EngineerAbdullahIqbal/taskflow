"""Storage layer with Protocol pattern for extensibility."""

from typing import Protocol, Optional
from src.models import Task


class StorageProtocol(Protocol):
    """Interface for task storage implementations.

    This protocol defines the contract that any storage backend must implement.
    Using Protocol enables structural subtyping (duck typing with types).
    """

    def add(self, task: Task) -> Task:
        """Add a task to storage and assign an ID.

        Args:
            task: Task with placeholder ID (0)

        Returns:
            Task with assigned sequential ID
        """
        ...

    def get_all(self) -> list[Task]:
        """Get all tasks from storage.

        Returns:
            List of all tasks, empty if none exist
        """
        ...

    def get(self, task_id: int) -> Optional[Task]:
        """Get a single task by ID.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Task if found, None otherwise
        """
        ...

    def update(self, task: Task) -> Task:
        """Update an existing task.

        Args:
            task: Task with updated fields

        Returns:
            Updated task
        """
        ...

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Returns:
            True if deleted, False if not found
        """
        ...


class InMemoryStorage:
    """In-memory implementation of StorageProtocol.

    Stores tasks in a Python list with sequential ID counter.
    No persistence - data lost when application exits.
    """

    def __init__(self) -> None:
        """Initialize in-memory storage."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add(self, task: Task) -> Task:
        """Add a task and assign sequential ID."""
        new_task = Task(
            id=self._next_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at
        )
        self._tasks.append(new_task)
        self._next_id += 1
        return new_task

    def get_all(self) -> list[Task]:
        """Get all tasks."""
        return list(self._tasks)

    def get(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task: Task) -> Task:
        """Update task in storage."""
        for i, stored_task in enumerate(self._tasks):
            if stored_task.id == task.id:
                self._tasks[i] = task
                return task
        return task

    def delete(self, task_id: int) -> bool:
        """Delete task by ID."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False
