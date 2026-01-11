from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.models.user import User, UserCreate, Profile
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_db

router = APIRouter()

@router.post("/signup")
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == user_in.email)).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        password_hash=hashed_password,
        role=user_in.role,
        level=user_in.level
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create profile
    profile = Profile(user_id=user.id)
    db.add(profile)
    db.commit()
    
    return {"message": "User created successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
