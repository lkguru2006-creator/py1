from datetime import datetime
from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Relationship, JSON, Column

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    role: str = Field(default="learner")
    level: str = Field(default="A1")
    goals: Optional[str] = None
    preferences_json: Optional[Dict] = Field(default={}, sa_column=Column(JSON))

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    profile: "Profile" = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

class Profile(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    streak: int = Field(default=0)
    xp: int = Field(default=0)
    coins: int = Field(default=0)
    selected_character: Optional[str] = Field(default="Luna")
    badges_json: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))

    user: User = Relationship(back_populates="profile")
