from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.lesson import Lesson, Note
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[Lesson])
def get_lessons(level: str = None, db: Session = Depends(get_db)):
    query = select(Lesson)
    if level:
        query = query.where(Lesson.level == level)
    return db.exec(query).all()

@router.get("/{lesson_id}", response_model=Lesson)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.post("/", response_model=Lesson)
def create_lesson(lesson: Lesson, db: Session = Depends(get_db)):
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson
