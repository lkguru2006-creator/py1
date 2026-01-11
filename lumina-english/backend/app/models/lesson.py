from datetime import datetime
from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Relationship, JSON, Column

class Lesson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    level: str  # A1, A2, B1, B2, C1
    objectives_json: Dict = Field(default={}, sa_column=Column(JSON))
    content_md: str
    quiz_json: Dict = Field(default={}, sa_column=Column(JSON))
    tags: Optional[str] = None
    published: bool = Field(default=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    lesson_id: Optional[int] = Field(default=None, foreign_key="lesson.id")
    title: str
    body_md: str
    is_personal: bool = Field(default=True)
    version: int = Field(default=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    date: datetime = Field(default_factory=datetime.utcnow)
    items_json: Dict = Field(default={}, sa_column=Column(JSON))
    completed_items_json: Dict = Field(default={}, sa_column=Column(JSON))
    status: str = Field(default="pending") # pending, completed
