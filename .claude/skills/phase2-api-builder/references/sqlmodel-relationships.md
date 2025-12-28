# SQLModel Relationship Patterns

## One-to-Many Relationships

**Pattern: User has many Tasks**

```python
# backend/app/models/user.py
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str

    # Relationship: One user → Many tasks
    tasks: list["Task"] = Relationship(back_populates="user")

# backend/app/models/task.py
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str

    # Relationship: Many tasks → One user
    user: User = Relationship(back_populates="tasks")
```

**Querying with Relationships**:

```python
# Get user with all tasks (eager loading)
from sqlmodel import select

user = db.exec(
    select(User)
    .where(User.id == user_id)
).first()

# Access tasks (already loaded)
print(user.tasks)  # list[Task]

# Get task with user info
task = db.exec(
    select(Task)
    .where(Task.id == task_id)
).first()

print(task.user.email)  # Access user data
```

**Cascade Delete** (Optional):

```python
class User(SQLModel, table=True):
    tasks: list["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

# When user is deleted, all their tasks are automatically deleted
db.delete(user)
db.commit()  # Tasks cascade deleted
```

## Many-to-Many Relationships

**Pattern: Tasks have many Tags (via TaskTag link table)**

```python
# backend/app/models/task_tag.py (Link table)
from sqlmodel import SQLModel, Field

class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)

# backend/app/models/task.py
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    title: str

    # Many-to-many: Task ↔ Tag
    tags: list["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTag
    )

# backend/app/models/tag.py
class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    # Many-to-many: Tag ↔ Task
    tasks: list[Task] = Relationship(
        back_populates="tags",
        link_model=TaskTag
    )
```

**Querying Many-to-Many**:

```python
# Get task with all tags
task = db.exec(
    select(Task)
    .where(Task.id == task_id)
).first()

print([tag.name for tag in task.tags])  # ['urgent', 'work']

# Add tag to task
new_tag = Tag(name="important")
task.tags.append(new_tag)
db.add(task)
db.commit()

# Remove tag from task
task.tags.remove(tag)
db.commit()
```

## Self-Referencing Relationships

**Pattern: Tasks can have subtasks (tree structure)**

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    title: str
    parent_id: int | None = Field(default=None, foreign_key="tasks.id")

    # Self-referencing: parent task → subtasks
    parent: "Task | None" = Relationship(
        back_populates="subtasks",
        sa_relationship_kwargs={"remote_side": "Task.id"}
    )
    subtasks: list["Task"] = Relationship(back_populates="parent")
```

**Querying Tree Structure**:

```python
# Get task with all subtasks
task = db.exec(
    select(Task)
    .where(Task.id == task_id)
).first()

for subtask in task.subtasks:
    print(f"  - {subtask.title}")

# Get parent task
if task.parent:
    print(f"Parent: {task.parent.title}")
```

## Optimized Queries (Avoid N+1 Problem)

**Problem: N+1 Queries**

```python
# BAD: This causes N+1 queries
tasks = db.exec(select(Task)).all()
for task in tasks:
    print(task.user.email)  # Separate query for EACH task
```

**Solution 1: Use `selectinload` (Eager Loading)**

```python
from sqlalchemy.orm import selectinload

# GOOD: 2 queries total (1 for tasks, 1 for users)
statement = select(Task).options(selectinload(Task.user))
tasks = db.exec(statement).all()

for task in tasks:
    print(task.user.email)  # No additional queries
```

**Solution 2: Use `joinedload` (Single Query with JOIN)**

```python
from sqlalchemy.orm import joinedload

# GOOD: 1 query with JOIN
statement = select(Task).options(joinedload(Task.user))
tasks = db.exec(statement).all()

for task in tasks:
    print(task.user.email)  # Already loaded
```

## Indexes for Performance

**Add indexes to foreign keys and frequently queried columns:**

```python
class Task(SQLModel, table=True):
    user_id: str = Field(foreign_key="users.id", index=True)  # Index for filtering by user
    completed: bool = Field(default=False, index=True)        # Index for filtering by status
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Index for sorting

# Composite index for common queries (user_id + completed)
__table_args__ = (
    Index("idx_user_completed", "user_id", "completed"),
)
```

## Soft Deletes (Optional Pattern)

```python
class Task(SQLModel, table=True):
    deleted_at: datetime | None = Field(default=None, index=True)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

# Soft delete method
def soft_delete(self):
    self.deleted_at = datetime.utcnow()

# Query only non-deleted tasks
statement = select(Task).where(Task.deleted_at.is_(None))
active_tasks = db.exec(statement).all()
```

## Migration Patterns (Alembic)

**Generate Migration for Relationship Changes**:

```bash
# After adding relationship to models
alembic revision --autogenerate -m "Add user-task relationship"

# Review migration file, then apply
alembic upgrade head
```

**Manual Migration for Complex Changes**:

```python
# migrations/versions/20251227_add_tags.py
def upgrade():
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'task_tags',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id']),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id']),
        sa.PrimaryKeyConstraint('task_id', 'tag_id')
    )

def downgrade():
    op.drop_table('task_tags')
    op.drop_table('tags')
```
