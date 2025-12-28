"""Service layer with business logic."""

from src.storage import StorageProtocol
from src.models import Task
from typing import Optional


class TaskManager:
    """Manages tasks via a storage backend.

    This service layer handles business logic for task operations,
    delegating persistence to the injected storage layer.
    """

    def __init__(self, storage: StorageProtocol) -> None:
        """Initialize TaskManager with a storage backend.

        Args:
            storage: An object implementing StorageProtocol
        """
        self._storage: StorageProtocol = storage

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description

        Returns:
            Created Task with assigned ID

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        if not title.strip():
            raise ValueError("Title cannot be empty")

        task = Task(
            id=0,  # Placeholder, storage will assign real ID
            title=title.strip(),
            description=description.strip(),
        )
        return self._storage.add(task)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all tasks, empty if none exist
        """
        return self._storage.get_all()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a single task by ID.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Task if found, None otherwise
        """
        return self._storage.get(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update an existing task.

        Args:
            task_id: ID of task to update
            title: New title (None = keep original)
            description: New description (None = keep original, "" = clear)

        Returns:
            Updated Task if found, None otherwise
        """
        task = self._storage.get(task_id)
        if task is None:
            return None

        updated_title = title.strip() if title else task.title
        updated_description = description.strip() if description is not None else task.description

        updated = Task(
            id=task.id,
            title=updated_title,
            description=updated_description,
            completed=task.completed,
            created_at=task.created_at
        )
        return self._storage.update(updated)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Returns:
            True if deleted, False if not found
        """
        return self._storage.delete(task_id)

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle task completion status.

        Args:
            task_id: ID of task to toggle

        Returns:
            Updated Task if found, None otherwise
        """
        task = self._storage.get(task_id)
        if task is None:
            return None

        updated = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=not task.completed,
            created_at=task.created_at
        )
        return self._storage.update(updated)
