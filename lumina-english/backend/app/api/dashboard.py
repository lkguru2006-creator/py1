from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.user import User, Profile
from app.models.lesson import Task
from app.api.deps import get_db
from app.api.user_deps import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/")
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.exec(select(Profile).where(Profile.user_id == current_user.id)).first()
    
    # Get today's tasks
    today = datetime.utcnow().date()
    # Simple query for tasks on this date (filtering in Python for SQLite simplicity or use func.date)
    all_tasks = db.exec(select(Task).where(Task.user_id == current_user.id)).all()
    today_tasks = [t for t in all_tasks if t.date.date() == today]
    
    if not today_tasks:
        # Auto-generate tasks if none exist (Mock generation for now)
        new_task = Task(
            user_id=current_user.id,
            date=datetime.utcnow(),
            items_json={
                "task1": "Complete A1 Lesson 1",
                "task2": "Play Vocab Match",
                "task3": "Write 5 sentences"
            },
            completed_items_json={},
            status="pending"
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        today_tasks = [new_task]

    return {
        "user": {
            "email": current_user.email,
            "level": current_user.level,
            "goals": current_user.goals
        },
        "profile": {
            "streak": profile.streak if profile else 0,
            "xp": profile.xp if profile else 0,
            "coins": profile.coins if profile else 0,
            "character": profile.selected_character if profile else "Luna"
        },
        "tasks": today_tasks[0] if today_tasks else None
    }
