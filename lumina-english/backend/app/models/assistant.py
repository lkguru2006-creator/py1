from datetime import datetime
from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Relationship, JSON, Column

class AssistantSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    mode: str = Field(default="Explain") # Explain, Practice, Translate, Quiz me
    context_json: Dict = Field(default={}, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AssistantMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="assistantsession.id", index=True)
    role: str # user, assistant, system
    content: str
    tokens_used: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
