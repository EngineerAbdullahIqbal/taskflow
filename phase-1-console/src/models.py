"""Data models for TaskFlow."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique sequential integer identifier
        title: Required task title (1-200 characters)
        description: Optional task description (0-1000 characters)
        completed: Whether the task is marked as done
        created_at: Timestamp when the task was created
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        """Return formatted task string: '[status] id. title'."""
        return f"{self.status_indicator} {self.id}. {self.title}"

    @property
    def status_indicator(self) -> str:
        """Return completion status indicator: '[ ]' or '[✓]'."""
        return "[✓]" if self.completed else "[ ]"
