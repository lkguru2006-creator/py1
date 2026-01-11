from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.assistant import AssistantSession, AssistantMessage
from app.models.user import User
from app.api.deps import get_db
from app.api.user_deps import get_current_user
from app.core.assistant import AssistantService
import os

router = APIRouter()
assistant_service = AssistantService(api_key=os.environ.get("GEMINI_API_KEY"))

@router.post("/session", response_model=AssistantSession)
def create_session(
    mode: str = "Explain",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = AssistantSession(user_id=current_user.id, mode=mode)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.post("/message")
async def send_message(
    session_id: int,
    content: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.get(AssistantSession, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    user_msg = AssistantMessage(session_id=session_id, role="user", content=content)
    db.add(user_msg)
    
    # Get history
    history = db.exec(
        select(AssistantMessage).where(AssistantMessage.session_id == session_id).order_by(AssistantMessage.created_at)
    ).all()
    
    # Get AI response
    try:
        response_text = await assistant_service.get_response(
            mode=session.mode,
            user_level=current_user.level,
            history=history,
            query=content
        )
    except Exception as e:
        response_text = "I'm having trouble connecting to my brain right now. Please try again later! (Error: API Key likely missing)"
    
    # Save assistant message
    assistant_msg = AssistantMessage(session_id=session_id, role="assistant", content=response_text)
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)
    
    return assistant_msg

@router.get("/session/{session_id}/messages", response_model=list[AssistantMessage])
def get_messages(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.get(AssistantSession, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = db.exec(
        select(AssistantMessage).where(AssistantMessage.session_id == session_id).order_by(AssistantMessage.created_at)
    ).all()
    return messages
