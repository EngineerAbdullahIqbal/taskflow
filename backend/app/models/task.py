"""Task model"""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Rich task/habit model with priority, categories, and scheduling"""

    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    story: str | None = Field(default=None, max_length=2000)
    priority: str = Field(default="medium", max_length=20, index=True)  # low/medium/high/urgent
    schedule: str | None = Field(default=None, max_length=500)  # JSON array for recurring days
    due_date: datetime | None = Field(default=None, index=True)
    category_id: int | None = Field(default=None, foreign_key="categories.id", index=True)
    reminder_enabled: bool = Field(default=False)
    reminder_timing: int | None = Field(default=None)  # Minutes before due_date
    reminder_channels: str | None = Field(default=None, max_length=50)  # email,browser
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
