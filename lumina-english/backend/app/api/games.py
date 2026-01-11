from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.games import Game, GameSession
from app.models.user import User, Profile
from app.api.deps import get_db
from app.api.user_deps import get_current_user

router = APIRouter()

@router.get("/", response_model=list[Game])
def get_games(db: Session = Depends(get_db)):
    return db.exec(select(Game)).all()

@router.post("/{game_id}/session")
def record_session(
    game_id: int,
    score: int,
    duration_sec: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
        
    session = GameSession(
        user_id=current_user.id,
        game_id=game_id,
        score=score,
        duration_sec=duration_sec
    )
    db.add(session)
    
    # Award XP and coins based on score
    xp_gained = score // 10
    coins_gained = score // 20
    
    profile = db.exec(select(Profile).where(Profile.user_id == current_user.id)).first()
    if profile:
        profile.xp += xp_gained
        profile.coins += coins_gained
        db.add(profile)
    
    db.commit()
    return {"xp_gained": xp_gained, "coins_gained": coins_gained}
