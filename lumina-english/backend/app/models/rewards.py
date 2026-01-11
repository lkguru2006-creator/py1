from datetime import datetime
from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Relationship, JSON, Column

class Reward(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str # cosmetic, badge, coin_pack
    key: str # unique identifier like 'luna_winter_skin'
    name: str
    description: str
    cost_coins: int = Field(default=0)
    unlock_rules_json: Dict = Field(default={}, sa_column=Column(JSON))

class UserReward(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    reward_id: int = Field(foreign_key="reward.id")
    unlocked_at: datetime = Field(default_factory=datetime.utcnow)

class Progress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    metric_key: str # daily_xp, lessons_completed, games_played
    value_num: float = Field(default=0)
    value_json: Dict = Field(default={}, sa_column=Column(JSON))
    date: datetime = Field(default_factory=datetime.utcnow)
