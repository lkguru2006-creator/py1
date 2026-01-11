from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.lesson import Note
from app.models.user import User
from app.api.deps import get_db
from app.api.user_deps import get_current_user

router = APIRouter()

@router.get("/", response_model=list[Note])
def get_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.exec(select(Note).where(Note.user_id == current_user.id)).all()

@router.post("/", response_model=Note)
def create_personal_note(
    note: Note,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note.user_id = current_user.id
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
