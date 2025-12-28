# Data Model: TaskFlow Console Application

**Date**: 2025-12-27
**Feature**: Phase 1 Console Application
**Source**: [spec.md](./spec.md) Key Entities section

## Entity Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                           Task                               │
├─────────────────────────────────────────────────────────────┤
│  id: int              [PK, auto-generated, sequential]      │
│  title: str           [required, 1-200 chars]               │
│  description: str     [optional, 0-1000 chars, default=""]  │
│  completed: bool      [default=False]                       │
│  created_at: datetime [auto-generated at creation]          │
├─────────────────────────────────────────────────────────────┤
│  Methods:                                                    │
│  • __str__() → "[status] id. title"                         │
│  • status_indicator → "[ ]" or "[✓]"                        │
└─────────────────────────────────────────────────────────────┘
```

## Entity: Task

### Purpose
Represents a single todo item in the TaskFlow application. Tasks are the core domain object around which all operations revolve.

### Attributes

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | int | Yes | Auto | Positive, unique, sequential | Unique identifier assigned by storage layer |
| `title` | str | Yes | - | 1-200 characters, non-blank | Primary description of the task |
| `description` | str | No | "" | 0-1000 characters | Additional details about the task |
| `completed` | bool | Yes | False | - | Whether the task has been marked done |
| `created_at` | datetime | Yes | now() | - | Timestamp when task was created |

### Validation Rules

| Rule ID | Field | Rule | Error Message |
|---------|-------|------|---------------|
| VR-001 | title | Cannot be empty or whitespace-only | "Title cannot be empty" |
| VR-002 | title | Length must be 1-200 characters | "Title must be 1-200 characters" |
| VR-003 | description | Length must be 0-1000 characters | "Description must be 0-1000 characters" |
| VR-004 | id | Must be positive integer | (System-generated, not user-facing) |

### State Transitions

```
                    ┌──────────────┐
                    │   Created    │
                    │ (pending)    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │  Update  │  │ Toggle   │  │  Delete  │
       │  (edit)  │  │ Complete │  │ (remove) │
       └────┬─────┘  └────┬─────┘  └──────────┘
            │             │
            │             ▼
            │      ┌──────────────┐
            │      │  Completed   │◄────┐
            │      │    [✓]       │     │
            │      └──────┬───────┘     │
            │             │             │
            │             ▼             │
            │      ┌──────────────┐     │
            └─────►│   Pending    │─────┘
                   │    [ ]       │ (toggle)
                   └──────────────┘
```

### Display Format

When displayed in the task list:

```
[status] id. title

Examples:
[ ] 1. Buy groceries
[✓] 2. Call mom
[ ] 3. Finish project report
```

### Relationships

Phase 1 has no relationships - Task is a standalone entity.

**Future Phases**:
- Phase 2+: Task may belong to a Project
- Phase 3+: Task may have Labels/Tags
- Phase 5+: Task may have Priority, DueDate

## Storage Model

### InMemoryStorage

```
┌─────────────────────────────────────────────────────────────┐
│                     InMemoryStorage                          │
├─────────────────────────────────────────────────────────────┤
│  _tasks: list[Task]    [internal storage]                   │
│  _next_id: int         [counter for ID generation]          │
├─────────────────────────────────────────────────────────────┤
│  Protocol Methods:                                           │
│  • add(task: Task) → Task                                   │
│  • get_all() → list[Task]                                   │
│  • get(id: int) → Task | None                               │
│  • update(task: Task) → Task                                │
│  • delete(id: int) → bool                                   │
└─────────────────────────────────────────────────────────────┘
```

### Storage Protocol (Interface)

```python
class StorageProtocol(Protocol):
    def add(self, task: Task) -> Task: ...
    def get_all(self) -> list[Task]: ...
    def get(self, id: int) -> Task | None: ...
    def update(self, task: Task) -> Task: ...
    def delete(self, id: int) -> bool: ...
```

### ID Generation

| Aspect | Behavior |
|--------|----------|
| Starting value | 1 |
| Increment | +1 for each new task |
| Reuse after delete | No (IDs never reused) |
| Maximum value | Limited by Python int (effectively unlimited) |

**Example Sequence**:
```
Add "Task A" → ID 1
Add "Task B" → ID 2
Delete ID 1
Add "Task C" → ID 3 (not 1)
```

## Type Definitions

### Python Implementation Signature

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        status = "✓" if self.completed else " "
        return f"[{status}] {self.id}. {self.title}"

    @property
    def status_indicator(self) -> str:
        return "[✓]" if self.completed else "[ ]"
```

## Sample Data

### Example Tasks (for testing)

```python
task1 = Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False,
    created_at=datetime(2025, 12, 27, 10, 30, 0)
)

task2 = Task(
    id=2,
    title="Call mom",
    description="",
    completed=True,
    created_at=datetime(2025, 12, 27, 11, 0, 0)
)

task3 = Task(
    id=3,
    title="Finish project report",
    description="Include Q4 metrics and recommendations",
    completed=False,
    created_at=datetime(2025, 12, 27, 14, 15, 0)
)
```

### Expected Display Output

```
Your Tasks:
  [ ] 1. Buy groceries
  [✓] 2. Call mom
  [ ] 3. Finish project report
```

## Evolution Path (Future Phases)

### Phase 2: Add persistence
- Task gains `updated_at` field
- Storage moves to PostgreSQL
- ID becomes UUID

### Phase 3: Add categories
- Task gains `priority` field (1-5)
- Task gains `due_date` field
- Task gains `labels` relationship

### Phase 5: Add collaboration
- Task gains `assigned_to` field
- Task gains `created_by` field
- Task gains `project_id` foreign key
