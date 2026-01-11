from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.user import User, Profile
from app.api.deps import get_db
from app.api.user_deps import get_current_user

router = APIRouter()

@router.get("/me")
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me")
def update_user_me(
    user_update: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    for key, value in user_update.items():
        setattr(current_user, key, value)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
