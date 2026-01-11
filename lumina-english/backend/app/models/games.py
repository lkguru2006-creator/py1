from datetime import datetime
from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Relationship, JSON, Column

class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str # vocab_match, sentence_builder, grammar_fix
    config_json: Dict = Field(default={}, sa_column=Column(JSON))
    enabled: bool = Field(default=True)

class GameSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    game_id: int = Field(foreign_key="game.id")
    score: int = Field(default=0)
    duration_sec: int = Field(default=0)
    metadata_json: Dict = Field(default={}, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
