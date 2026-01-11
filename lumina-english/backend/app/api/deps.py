from sqlmodel import Session, create_engine, SQLModel
from typing import Generator

sqlite_url = "sqlite:///./lumina.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator:
    with Session(engine) as session:
        yield session
