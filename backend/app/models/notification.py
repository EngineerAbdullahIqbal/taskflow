"""Notification model"""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Notification(SQLModel, table=True):
    """Notification history model (30-day retention)"""

    __tablename__ = "notifications"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    task_id: int | None = Field(default=None, foreign_key="tasks.id")
    type: str = Field(max_length=50)  # reminder, task_complete, etc.
    title: str = Field(max_length=200)
    message: str = Field(max_length=500)
    read: bool = Field(default=False, index=True)
    clicked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
