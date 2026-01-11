from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, lessons, dashboard, assistant, rewards, games, notes

from app.api.deps import create_db_and_tables, engine
from app.core.seed import seed_data
from sqlmodel import Session

app = FastAPI(title="Lumina English API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        seed_data(session)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Lumina English API"}

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(assistant.router, prefix="/assistant", tags=["assistant"])
app.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
app.include_router(games.router, prefix="/games", tags=["games"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
