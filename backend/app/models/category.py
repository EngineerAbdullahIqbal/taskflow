"""Category model"""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    """Task category model (max 20 per user)"""

    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=100)
    color: str = Field(max_length=7)  # Hex color code #RRGGBB
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
