"""Notification preference model"""

from datetime import datetime

from sqlmodel import Field, SQLModel


class NotificationPreference(SQLModel, table=True):
    """User notification preferences"""

    __tablename__ = "notification_preferences"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, index=True)
    reminder_email: str | None = Field(default=None, max_length=255)
    email_notifications_enabled: bool = Field(default=True)
    browser_notifications_enabled: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
