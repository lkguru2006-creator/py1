from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.rewards import Reward, UserReward
from app.models.user import User, Profile
from app.api.deps import get_db
from app.api.user_deps import get_current_user

router = APIRouter()

@router.get("/", response_model=list[Reward])
def get_rewards(db: Session = Depends(get_db)):
    return db.exec(select(Reward)).all()

@router.post("/{reward_id}/unlock")
def unlock_reward(
    reward_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reward = db.get(Reward, reward_id)
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    
    # Check if already unlocked
    existing = db.exec(
        select(UserReward).where(UserReward.user_id == current_user.id, UserReward.reward_id == reward_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already unlocked")
    
    # Check coins
    profile = db.exec(select(Profile).where(Profile.user_id == current_user.id)).first()
    if profile.coins < reward.cost_coins:
        raise HTTPException(status_code=400, detail="Not enough coins")
    
    # Dedact coins and unlock
    profile.coins -= reward.cost_coins
    db.add(profile)
    
    user_reward = UserReward(user_id=current_user.id, reward_id=reward_id)
    db.add(user_reward)
    db.commit()
    
    return {"message": f"Successfully unlocked {reward.name}"}
